# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import nukescripts
import nuke
import sgtk
from sgtk import TankError
from sgtk.platform.qt import QtCore, QtGui

from .ui.dialog import Ui_Dialog

logger = sgtk.platform.get_logger(__name__)

overlay_widget = sgtk.platform.import_framework("tk-framework-qtwidgets", "overlay_widget")

class Dialog(QtGui.QWidget):
    """
    Main dialog window for the App
    """

    def __init__(self, parent=None):
        """
        :param parent: The parent QWidget for this control
        """
        QtGui.QWidget.__init__(self, parent)

        self._bundle = sgtk.platform.current_bundle()

        # set up the UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

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

    def _setup_formatting(self, group_node, sg_version_name):
        """
        Sets up slates and burnins
        """

        # set the fonts for all text fields
        font = os.path.join(self.disk_location, "resources", "OpenSans-Regular.ttf")
        font = font.replace(os.sep, "/")
        group_node.node("top_left_text")["font"].setValue(font)
        group_node.node("top_right_text")["font"].setValue(font)
        group_node.node("bottom_left_text")["font"].setValue(font)
        group_node.node("framecounter")["font"].setValue(font)
        group_node.node("slate_info")["font"].setValue(font)

        # get some useful data

        # date -- format '23 Jan 2012' is universally understood.
        today = datetime.date.today()
        date_formatted = today.strftime("%d %b %Y")

        # current user
        user_data = sgtk.util.get_current_user(self.sgtk)
        if user_data is None:
            user_name = "Unknown User"
        else:
            user_name = user_data.get("name", "Unknown User")

            # format the burnins

        # top-left says
        # Project XYZ
        # Shot ABC
        top_left = "%s" % self.context.project["name"]
        if self.context.entity:
            top_left += "\n%s %s" % (self.context.entity["type"], self.context.entity["name"])

        group_node.node("top_left_text")["message"].setValue(top_left)

        # top-right has date
        group_node.node("top_right_text")["message"].setValue(date_formatted)

        # bottom left says
        # Name#increment
        # User
        bottom_left = "%s\n%s" % (sg_version_name, user_name)
        group_node.node("bottom_left_text")["message"].setValue(bottom_left)

        # and the slate
        slate_str = "Project: %s\n" % self.context.project["name"]
        if self.context.entity:
            slate_str += "%s: %s\n" % (self.context.entity["type"], self.context.entity["name"])
        slate_str += "Name: %s\n" % sg_version_name

        if self.context.task:
            slate_str += "Task: %s\n" % self.context.task["name"]
        elif self.context.step:
            slate_str += "Step: %s\n" % self.context.step["name"]

        slate_str += "Frames: %s - %s\n" % (self._get_first_frame(), self._get_last_frame())
        slate_str += "Date: %s\n" % date_formatted
        slate_str += "User: %s\n" % user_name

        group_node.node("slate_info")["message"].setValue(slate_str)

    def _render(self, group_node, mov_path):
        """
        Renders quickdaily node
        """
        # setup quicktime output resolution
        width = 1280
        height = 720
        mov_reformat_node = group_node.node("mov_reformat")
        mov_reformat_node["box_width"].setValue(width)
        mov_reformat_node["box_height"].setValue(height)

        # setup output quicktime path
        mov_out = group_node.node("mov_writer")
        mov_path = mov_path.replace(os.sep, "/")
        mov_out["file"].setValue(mov_path)

        # apply the Write node codec settings we'll use for generating the Quicktime
        self.execute_hook_method("codec_settings_hook",
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

    def _get_comments(self, sg_version_name):
        """
        Get name and comments from user via UI
        """
        # deferred import so that this app runs in batch mode
        tk_nuke_quickreview = self.import_module("tk_nuke_quickreview")
        d = tk_nuke_quickreview.CommentsPanel(sg_version_name)
        result = d.showModalDialog()
        if result:
            return d.get_comments()
        else:
            return None

    def submit(self, group_node):
        """
        Called from the gizmo when the review button is pressed.
        Creates
        """

        tk_nuke_quickreview = self.import_module("tk_nuke_quickreview")
        self.engine.show_dialog("Submit for Review", self, tk_nuke_quickreview.Dialog)

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
        message = self._get_comments(sg_version_name)
        if message is None:
            # user pressed cancel!
            return

        # set metadata
        self._setup_formatting(group_node, sg_version_name)

        # generate temp file for mov sequence
        mov_folder = tempfile.mkdtemp()
        mov_path = os.path.join(mov_folder, "%s.mov" % quicktime_filename)

        # and render!
        self._render(group_node, mov_path)

        # create sg version
        data = {
            "code": sg_version_name,
            "description": message,
            "project": self.context.project,
            "entity": self.context.entity,
            "sg_task": self.context.task,
            "created_by": sgtk.util.get_current_user(self.sgtk),
            "user": sgtk.util.get_current_user(self.sgtk),
            "sg_first_frame": self._get_first_frame(),
            "sg_last_frame": self._get_last_frame(),
            "frame_count": (self._get_last_frame() - self._get_first_frame()) + 1,
            "frame_range": "%d-%d" % (self._get_first_frame(), self._get_last_frame()),
            "sg_movie_has_slate": True
        }

        entity = self.shotgun.create("Version", data)
        self.log_debug("Version created in Shotgun %s" % entity)

        # upload the movie to Shotgun if desired
        self.log_debug("Uploading movie to Shotgun")
        self.shotgun.upload("Version", entity["id"], mov_path, "sg_uploaded_movie")

        # execute post hook
        self.log_debug("Running post hooks...")
        for h in self.get_setting("post_hooks", []):
            self.execute_hook_by_name(h, shotgun_data=entity)

        # status message!
        sg_url = "%s/detail/Version/%s" % (self.shotgun.base_url, entity["id"])
        nuke.message("Your submission was successfully sent to review.")







