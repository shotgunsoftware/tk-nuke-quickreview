# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import nuke
import sgtk
import datetime
import tempfile
from sgtk import TankError
from sgtk.platform.qt import QtCore, QtGui

from .ui.dialog import Ui_Dialog

logger = sgtk.platform.get_logger(__name__)
overlay = sgtk.platform.import_framework("tk-framework-qtwidgets", "overlay_widget")
sg_data = sgtk.platform.import_framework("tk-framework-shotgunutils", "shotgun_data")
task_manager = sgtk.platform.import_framework("tk-framework-shotgunutils", "task_manager")


class Dialog(QtGui.QWidget):
    """
    Main dialog window for the App
    """

    def __init__(self, nuke_review_node, parent=None):
        """
        :param nuke_review_node: Selected nuke gizmo to render.
        :param parent: The parent QWidget for this control
        """
        QtGui.QWidget.__init__(self, parent)

        self._bundle = sgtk.platform.current_bundle()
        self._group_node = nuke_review_node


        self._task_manager = task_manager.BackgroundTaskManager(parent=self,
                                                                start_processing=True,
                                                                max_threads=2)


        # set up data retriever
        self.__sg_data = sg_data.ShotgunDataRetriever(self)
        self.__sg_data.work_completed.connect(self.__on_worker_signal)
        self.__sg_data.work_failure.connect(self.__on_worker_failure)
        self.__sg_data.start()

        # set up the UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.context_widget.set_up(self._task_manager)
        self.ui.context_widget.context_changed.connect(self._on_item_context_change)


        self._overlay = overlay.ShotgunOverlayWidget(self)
        self.ui.submit.clicked.connect(self._submit)
        self.ui.cancel.clicked.connect(self.close)

        # set up basic UI
        self.ui.frame_range.setText(
            "Frame Range: %s-%s" % (self._get_first_frame(), self._get_last_frame())
        )
        self.ui.association.setText("Associated with: %s" % self._bundle.context)
        self.ui.association.setToolTip(
            "Your review version in Shotgun will be "
            "associated with this context. To change this, "
            "change your work area using the shotgun panel "
            "or file manager."
        )
        self.ui.title.setText(self._generate_title())

        # set focus on comments text box.
        self.ui.comments.setFocus()

    def closeEvent(self, event):
        """
        Executed when the dialog is closed.
        """
        try:
            self.__sg_data.stop()
        except Exception:
            logger.exception("Error running Loader App closeEvent()")

        # okay to close dialog
        event.accept()

    def _get_first_frame(self):
        """
        Returns the first frame for this session
        """
        return int(nuke.root()["first_frame"].value())

    def _get_last_frame(self):
        """
        Returns the last frame for this session
        """
        return int(nuke.root()["last_frame"].value())

    def _generate_title(self):
        """
        Create a title for the version
        """
        return self._bundle.execute_hook_method("settings_hook", "get_title")

    def _setup_formatting(self, sg_version_name):
        """
        Sets up slates and burnins
        """
        # set the fonts for all text fields
        font = os.path.join(self._bundle.disk_location, "resources", "OpenSans-Regular.ttf")
        font = font.replace(os.sep, "/")
        self._group_node.node("top_left_text")["font"].setValue(font)
        self._group_node.node("top_right_text")["font"].setValue(font)
        self._group_node.node("bottom_left_text")["font"].setValue(font)
        self._group_node.node("framecounter")["font"].setValue(font)
        self._group_node.node("slate_info")["font"].setValue(font)

        # get burnins and slate info from hook
        fields_dict = self._bundle.execute_hook_method(
            "settings_hook",
            "get_burnins_and_slate",
            sg_version_name=sg_version_name
        )

        # set up burnins
        self._group_node.node("top_left_text")["message"].setValue(fields_dict["top_left"])
        self._group_node.node("top_right_text")["message"].setValue(fields_dict["top_right"])
        self._group_node.node("bottom_left_text")["message"].setValue(fields_dict["bottom_left"])
        # note: bottom right is used as a default framecounter.

        # set up slate
        self._group_node.node("slate_info")["message"].setValue("\n".join(fields_dict["slate"]))

    @sgtk.LogManager.log_timing
    def _render(self, mov_path):
        """
        Renders write node

        :param mov_path: temporary path where quicktime should be written
        """
        # setup quicktime output resolution
        (width, height) = self._bundle.execute_hook_method(
            "settings_hook",
            "get_resolution"
        )

        mov_reformat_node = self._group_node.node("mov_reformat")
        mov_reformat_node["box_width"].setValue(width)
        mov_reformat_node["box_height"].setValue(height)

        # setup output quicktime path
        mov_out = self._group_node.node("mov_writer")
        mov_path = mov_path.replace(os.sep, "/")
        mov_out["file"].setValue(mov_path)

        # apply the Write node codec settings we'll use for generating the Quicktime
        self._bundle.execute_hook_method(
            "settings_hook",
            "setup_quicktime_node",
            write_node=mov_out
        )

        # turn on the node
        mov_out.knob("disable").setValue(False)

        # render everything - default to using the first view on stereo
        logger.debug("Rendering quicktime")
        try:
            first_view = nuke.views()[0]
            nuke.executeMultiple(
                [mov_out],
                ([self._get_first_frame() - 1, self._get_last_frame(), 1],),
                [first_view]
            )
        finally:
            # turn off the nodes again
            mov_out.knob("disable").setValue(True)

    def _navigate_to_version_and_close(self, panel_app, version_id):
        """
        Navigates to the given version in the given panel app
        and then closes this window.
        """
        panel_app.navigate("Version", version_id, panel_app.NEW_DIALOG)
        self.close()

    def _submit(self):
        """
        Submits the render for review.
        """
        try:
            self._overlay.start_spin()
            self._version_id = self._run_submission()

        except Exception, e:
            logger.exception("An exception was raised.")
            self._overlay.show_error_message("An error was reported: %s" % e)

    def _upload_to_shotgun(self, shotgun, data):
        """
        Upload quicktime to Shotgun.

        :param int version_id: Version id to upload to
        :param str file_name: Quicktime to upload
        """
        logger.debug("Uploading movie to Shotgun...")
        try:
            shotgun.upload(
                "Version",
                data["version_id"],
                data["file_name"],
                "sg_uploaded_movie"
            )
            logger.debug("...Upload complete!")
        finally:
            sgtk.util.filesystem.safe_delete_file(data["file_name"])

    def _run_submission(self):
        """
        Carry out the render and upload.
        """
        # get inputs - these come back as unicode so make sure convert to utf-8
        version_title = self.ui.title.text()
        if isinstance(version_title, unicode):
            version_title = version_title.encode("utf-8")

        message = self.ui.comments.toPlainText()
        if isinstance(message, unicode):
            message = message.encode("utf-8")

        # set metadata
        self._setup_formatting(version_title)

        # generate temp file for mov sequence
        mov_path = os.path.join(tempfile.gettempdir(), "quickreview.mov")
        mov_path = sgtk.util.filesystem.get_unused_path(mov_path)

        # and render!
        self._render(mov_path)

        # create sg version
        data = {
            "code": version_title,
            "description": message,
            "project": self._bundle.context.project,
            "entity": self._bundle.context.entity,
            "sg_task": self._bundle.context.task,
            "created_by": sgtk.util.get_current_user(self._bundle.sgtk),
            "user": sgtk.util.get_current_user(self._bundle.sgtk),
            "sg_first_frame": self._get_first_frame(),
            "sg_last_frame": self._get_last_frame(),
            "frame_count": (self._get_last_frame() - self._get_first_frame()) + 1,
            "frame_range": "%d-%d" % (self._get_first_frame(), self._get_last_frame()),
            "sg_movie_has_slate": True
        }

        entity = self._bundle.shotgun.create("Version", data)
        logger.debug("Version created in Shotgun %s" % entity)

        data = {"version_id": entity["id"], "file_name": mov_path}
        self.__sg_data.execute_method(self._upload_to_shotgun, data)

        return entity["id"]

    def __on_worker_failure(self, uid, msg):
        """
        Asynchronous callback - the worker thread errored.
        """
        self._overlay.show_error_message("An error was reported: %s" % msg)
        self.ui.submit.hide()
        self.ui.cancel.setText("Close")

    def __on_worker_signal(self, uid, request_type, data):
        """
        Signaled whenever the worker completes something.
        """
        self._overlay.hide()
        # show success screen
        self.ui.stack_widget.setCurrentIndex(1)
        # show button if we have panel loaded
        found_panel = False
        for app in self._bundle.engine.apps.values():
            if app.name == "tk-multi-shotgunpanel":
                # panel is loaded
                launch_panel_fn = lambda panel_app=app: self._navigate_to_version_and_close(
                    panel_app,
                    self._version_id
                )
                self.ui.jump_to_review.clicked.connect(launch_panel_fn)
                found_panel = True

        if not found_panel:
            # no panel, so hide button
            self.ui.jump_to_review.hide()

        # hide submit button, turn cancel button into a close button
        self.ui.submit.hide()
        self.ui.cancel.setText("Close")
