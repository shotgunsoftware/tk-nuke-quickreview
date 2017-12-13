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

class Dialog(QtGui.QWidget):
    """
    Main dialog window for the App
    """

    def __init__(self, nuke_review_node, parent=None):
        """
        :param parent: The parent QWidget for this control
        """
        QtGui.QWidget.__init__(self, parent)

        self._bundle = sgtk.platform.current_bundle()


        # set up the UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self._overlay = overlay.ShotgunOverlayWidget(self)

        self._group_node = nuke_review_node

        self.ui.submit.clicked.connect(self._submit)
        self.ui.cancel.clicked.connect(self.close)

    def _get_first_frame(self):
        """
        returns the first frame for this session
        """
        return int(nuke.root()["first_frame"].value())

    def _get_last_frame(self):
        """
        returns the last frame for this session
        """
        return int(nuke.root()["last_frame"].value())

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

        # get some useful data

        # date -- format '23 Jan 2012' is universally understood.
        today = datetime.date.today()
        date_formatted = today.strftime("%d %b %Y")

        # current user
        user_data = sgtk.util.get_current_user(self._bundle.sgtk)
        if user_data is None:
            user_name = "Unknown User"
        else:
            user_name = user_data.get("name", "Unknown User")

            # format the burnins

        # top-left says
        # Project XYZ
        # Shot ABC
        top_left = "%s" % self._bundle.context.project["name"]
        if self._bundle.context.entity:
            top_left += "\n%s %s" % (self._bundle.context.entity["type"], self._bundle.context.entity["name"])

        self._group_node.node("top_left_text")["message"].setValue(top_left)

        # top-right has date
        self._group_node.node("top_right_text")["message"].setValue(date_formatted)

        # bottom left says
        # Name#increment
        # User
        bottom_left = "%s\n%s" % (sg_version_name, user_name)
        self._group_node.node("bottom_left_text")["message"].setValue(bottom_left)

        # and the slate
        slate_str = "Project: %s\n" % self._bundle.context.project["name"]
        if self._bundle.context.entity:
            slate_str += "%s: %s\n" % (self._bundle.context.entity["type"], self._bundle.context.entity["name"])
        slate_str += "Name: %s\n" % sg_version_name

        if self._bundle.context.task:
            slate_str += "Task: %s\n" % self._bundle.context.task["name"]
        elif self._bundle.context.step:
            slate_str += "Step: %s\n" % self._bundle.context.step["name"]

        slate_str += "Frames: %s - %s\n" % (self._get_first_frame(), self._get_last_frame())
        slate_str += "Date: %s\n" % date_formatted
        slate_str += "User: %s\n" % user_name

        self._group_node.node("slate_info")["message"].setValue(slate_str)

    def _render(self, mov_path):
        """
        Renders quickdaily node
        """
        # setup quicktime output resolution
        width = 1280
        height = 720
        mov_reformat_node = self._group_node.node("mov_reformat")
        mov_reformat_node["box_width"].setValue(width)
        mov_reformat_node["box_height"].setValue(height)

        # setup output quicktime path
        mov_out = self._group_node.node("mov_writer")
        mov_path = mov_path.replace(os.sep, "/")
        mov_out["file"].setValue(mov_path)

        # apply the Write node codec settings we'll use for generating the Quicktime
        self._bundle.execute_hook_method("codec_settings_hook",
                                 "get_quicktime_settings",
                                 write_node=mov_out)

        # turn on the nodes
        mov_out.knob('disable').setValue(False)

        # finally render everything!
        # default to using the first view on stereo
        try:
            first_view = nuke.views()[0]
            nuke.executeMultiple(
                [mov_out],
                ([self._get_first_frame() - 1, self._get_last_frame(), 1],),
                [first_view]
            )
        finally:
            # turn off the nodes again
            mov_out.knob('disable').setValue(True)

    def _submit(self):
        """
        Submits the render for review.
        """
        try:
            self._overlay.start_spin()
            version_id = self._run_submission()
        except Exception, e:
            logger.exception("Something bad happened.")
            self._overlay.show_error_message("An error was reported: %s" % e)
        else:
            self._overlay.hide()
            # show success screen
            self.ui.stack_widget.setCurrentIndex(1)
            # todo: button
        finally:
            # buttons
            pass

    def _run_submission(self):
        """
        Called from the gizmo when the review button is pressed.
        Creates
        """
        name = "Quickdaily"

        # now try to see if we are in a normal work file
        # in that case deduce the name from it
        current_scene_path = nuke.root().name()
        if current_scene_path and current_scene_path != "Root":
            current_scene_path = current_scene_path.replace("/", os.path.sep)
            # get just filename
            current_scene_name = os.path.basename(current_scene_path)
            # drop .nk
            current_scene_name = os.path.splitext(current_scene_name)[0]
            name = current_scene_name

        # append date and time
        timestamp = datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")
        timestamp_filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        sg_version_name = "%s %s" % (name, timestamp)
        quicktime_filename = "%s_%s" % (name, timestamp_filename)

        # get inputs
        message = self.ui.comments.toPlainText()

        # set metadata
        self._setup_formatting(sg_version_name)

        # generate temp file for mov sequence
        mov_folder = tempfile.mkdtemp()
        mov_path = os.path.join(mov_folder, "%s.mov" % quicktime_filename)

        # and render!
        self._render(mov_path)

        # create sg version
        data = {
            "code": sg_version_name,
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

        # upload the movie to Shotgun if desired
        logger.debug("Uploading movie to Shotgun")
        self._bundle.shotgun.upload("Version", entity["id"], mov_path, "sg_uploaded_movie")

        return entity["id"]



