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


class ReviewEvents(HookBaseClass):
    """
    This hook exposes main events in the review workflow, allowing
    for various data injections and post processing.
    """

    def before_version_creation(self, sg_version_data):
        """
        Called before the version entity is created, allowing
        for injections of additional metadata or fields before
        anything has been added to shotgun.

        :param dict sg_version_data: Shotgun version dictionary
        :returns: Modified Shotgun version dictionary
        """
        raise NotImplementedError

    def after_version_creation(self, sg_version_id):
        """
        Called after the version entity has been created, but before
        any media upload has taken place.

        :param int sg_version_id: The associated version id
        """
        raise NotImplementedError

    def after_upload(self, sg_version_id):
        """
        Called after the media has been uplaoded to Shotgun.

        :param int sg_version_id: The associated version id
        """
        raise NotImplementedError
