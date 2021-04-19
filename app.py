# Copyright (c) 2017 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.


import sgtk
import nuke
import os


class NukeQuickReview(sgtk.platform.Application):
    """
    App that creates a Nuke node that sends items to Shotgun for review.
    """

    def init_app(self):
        """
        Called as the application is being initialized
        """
        # assign this app to nuke handle so that the gizmo finds it
        nuke.tk_nuke_quickreview = self

        # make the base plugins available via the app
        tk_nuke_quickreview = self.import_module("tk_nuke_quickreview")
        self._base_hooks = tk_nuke_quickreview.base_hooks

        # add to nuke node menu
        icon = os.path.join(self.disk_location, "resources", "node_icon.png")

        self.engine.register_command(
            "SG Quick Review", self.create_node, {"type": "node", "icon": icon}
        )

    @property
    def base_hooks(self):
        """
        Exposes the ``base_hooks`` module.

        This module provides base class implementations hooks.

        Access to these classes won't typically be needed when writing hooks as
        they are are injected into the class hierarchy automatically for any
        collector or publish plugins configured.

        :return: A handle on the app's ``base_hooks`` module.
        """
        return self._base_hooks

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
        nk_file = os.path.join(
            self.disk_location, "resources", "tk_nuke_quickreview.nk"
        )
        nk_file = nk_file.replace(os.sep, "/")
        nuke.nodePaste(nk_file)

    def create_review(self, group_node):
        """
        Called from the gizmo when the review button is pressed.

        :param group_node: The nuke node that was clicked.
        """
        tk_nuke_quickreview = self.import_module("tk_nuke_quickreview")
        self.engine.show_dialog(
            "Submit for Review",
            self,
            tk_nuke_quickreview.Dialog,
            nuke_review_node=group_node,
        )
