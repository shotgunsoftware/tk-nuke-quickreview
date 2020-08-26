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

HookBaseClass = sgtk.get_hook_baseclass()


class ReviewSettings(HookBaseClass):
    """
    This hook allows a user to customize and override default metadata, default
    values as well as controlling the format for the uploaded media.
    """

    def get_burnins_and_slate(self, sg_version_name, context):
        """
        Returns the burnins and slates that should be rendered into the review submission.

        Should return a dictionary with the following keys and format::

            {
                "slate": ["Name: lighting.v003.nk", "Date: 12 October 2001", "..."]
                "top_right": "Top right burnin"
                "top_left": "Top left burnin"
                "bottom_left": "Bottom left burnin"
            }

        .. note::
            The bottom right burn-in is used as a frame counter and is
            controlled by the app.

        :param str sg_version_name: The name of the shotgun review version
        :param context: The context associated with the version.
        :type context: :class:`~sgtk:sgtk.Context`
        :returns: Dictionary with burn-ins and slate strings
        """
        raise NotImplementedError

    def get_title(self, context):
        """
        Returns the title that should be used for the version.
        This value is presented in the UI to the user as a default value
        which can be manually updated.

        :param context: The context to be associated with the version.
        :type context: :class:`~sgtk:sgtk.Context`
        :returns: Version title string.
        """
        raise NotImplementedError

    def get_resolution(self):
        """
        Returns the resolution that should be used when rendering the quicktime.

        :returns: tuple with (width, height)
        """
        raise NotImplementedError

    def setup_quicktime_node(self, write_node):
        """
        Allows modifying settings for Quicktime generation.

        :param write_node: The nuke write node used to generate the quicktime that is being uploaded.
        """
        raise NotImplementedError
