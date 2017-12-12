# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Quick versions to shotgun from Nuke

"""

import sgtk
import nuke
import os

class NukeQuickReview(sgtk.platform.Application):
    """
    Toolkit App which sends items to Shotgun for review.
    """

    def init_app(self):
        """
        Called as the application is being initialized
        """
        
        # assign this app to nuke handle so that the node
        # callback finds it
        nuke.tk_nuke_quickreview = self

        # add to sgtk menu
        icon = os.path.join(self.disk_location, "resources", "node_icon.png")
        self.engine.register_command(
            "Shotgun Quick Review",
            self.create_node,
            {"type": "node", "icon": icon}
        )

    @property
    def context_change_allowed(self):
        """
        Specifies that context changes are allowed.
        """
        return True
                      
    def create_node(self):
        """
        Creates a quick review node
        """
        nk_file = os.path.join(self.disk_location, "resources", "tk_nuke_quickreview.nk")
        nk_file = nk_file.replace(os.sep, "/")
        nuke.nodePaste(nk_file)


    def create_review(self, group_node):
        """
        Called from the gizmo when the review button is pressed.
        """
        tk_nuke_quickreview = self.import_module("tk_nuke_quickreview")
        self.engine.show_dialog("Submit for Review", self, tk_nuke_quickreview.Dialog)

