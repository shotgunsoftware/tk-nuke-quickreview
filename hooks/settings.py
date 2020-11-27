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
import sys
import os
import nuke
import datetime

from tank_vendor import six

HookBaseClass = sgtk.get_hook_baseclass()


class Settings(HookBaseClass):
    """
    Controls various review settings and formatting.
    """

    def get_burnins_and_slate(self, sg_version_name, context):
        """
        Return the burnins that should be used for the quicktime.

        :param str sg_version_name: The name of the shotgun review version
        :param context: The context associated with the version.
        :returns: Dictionary with burn-ins and slate strings
        """
        return_data = {}

        # current user
        user_data = sgtk.util.get_current_user(self.parent.sgtk)
        if user_data is None:
            user_name = "Unknown User"
        else:
            user_name = user_data.get("name", "Unknown User")

        # top-left says
        # Project XYZ
        # Shot ABC
        top_left = "%s" % context.project["name"]
        if context.entity:
            top_left += "\n%s %s" % (context.entity["type"], context.entity["name"])
        return_data["top_left"] = top_left

        # top-right has date
        # The format '23 Jan 2012' is universally understood.
        today = datetime.date.today()
        date_formatted = today.strftime("%d %b %Y")
        return_data["top_right"] = date_formatted

        # bottom left says
        # sg version name
        # User
        bottom_left = "%s\n%s" % (sg_version_name, user_name)
        return_data["bottom_left"] = bottom_left

        # and format the slate
        slate_items = []
        slate_items.append("Project: %s" % context.project["name"])
        if context.entity:
            slate_items.append(
                "%s: %s" % (context.entity["type"], context.entity["name"])
            )
        slate_items.append("Name: %s" % sg_version_name)

        if context.task:
            slate_items.append("Task: %s" % context.task["name"])
        elif context.step:
            slate_items.append("Step: %s" % context.step["name"])

        slate_items.append("Date: %s" % date_formatted)
        slate_items.append("User: %s" % user_name)

        return_data["slate"] = slate_items

        return return_data

    def get_title(self, context):
        """
        Returns the title that should be used for the version

        :param context: The context associated with the version.
        :returns: Version title string.
        """
        # rather than doing a version numbering scheme, which we
        # reserve for publishing workflows, the default implementation
        # uses a date and time based naming scheme

        sg_version_name = ""

        # include the shot/link as part of the name
        # if context.entity and context.entity["name"]:
        #     # start with the link
        #     sg_version_name += "[%s %s] " % (
        #         context.entity["type"],
        #         context.entity["name"]
        #     )

        # default name in case no nuke file name is set
        name = "Quickreview"

        # now try to see if we are in a normal work file
        # in that case deduce the name from it
        current_scene_path = nuke.root().name()
        current_scene_path = six.ensure_str(current_scene_path)

        if current_scene_path and current_scene_path != "Root":
            current_scene_path = current_scene_path.replace("/", os.path.sep)
            # get just filename
            current_scene_name = os.path.basename(current_scene_path)
            # drop .nk
            current_scene_name = os.path.splitext(current_scene_name)[0]
            name = current_scene_name.replace("_", " ").capitalize()

        sg_version_name += name

        # append date and time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        sg_version_name += ", %s" % timestamp

        return sg_version_name

    def get_resolution(self):
        """
        Returns the resolution that should be used when rendering the quicktime.

        :returns: tuple with (width, height)
        """
        return 1280, 720

    def setup_quicktime_node(self, write_node):
        """
        Allows modifying settings for Quicktime generation.

        :param write_node: The nuke write node used to generate the quicktime that is being uploaded.
        """
        if sgtk.util.is_linux():
            if nuke.NUKE_VERSION_MAJOR >= 9:
                # Nuke 9.0v1 removed ffmpeg and replaced it with the mov64 writer
                # http://help.thefoundry.co.uk/nuke/9.0/#appendices/appendixc/supported_file_formats.html
                write_node["file_type"].setValue("mov64")
                write_node["mov64_codec"].setValue("jpeg")
                write_node["mov64_quality_max"].setValue("3")
            else:
                # the 'codec' knob name was changed to 'format' in Nuke 7
                write_node["file_type"].setValue("ffmpeg")
                write_node["format"].setValue("MOV format (mov)")
        elif nuke.NUKE_VERSION_MAJOR > 10 or (
            nuke.NUKE_VERSION_MAJOR == 10
            and (nuke.NUKE_VERSION_MINOR > 1 or nuke.NUKE_VERSION_RELEASE > 1)
        ):
            # In Nuke 10.0v2, the dependency on the Quicktime desktop application was removed. Because of
            # that, we have to account for changes in the .mov encoding settings in the Write node.
            write_node["file_type"].setValue("mov64")
            write_node["meta_codec"].setValue("jpeg")
            write_node["mov64_quality_max"].setValue("3")
        else:
            write_node["file_type"].setValue("mov")
            if nuke.NUKE_VERSION_MAJOR >= 9:
                # Nuke 9.0v1 changed the codec knob name to meta_codec and added an encoder knob
                # (which defaults to the new mov64 encoder/decoder).
                write_node["meta_codec"].setValue("jpeg")
                write_node["mov64_quality_max"].setValue("3")
            else:
                write_node["codec"].setValue("jpeg")
            write_node["fps"].setValue(23.97599983)
            # note: in older versions of nuke, this settings string represents all the quicktime
            # code settings used on windows and mac.
            write_node["settings"].setValue(
                "000000000000000000000000000019a7365616e0000000100000001000000000000018676696465000000010000000e00000000000000227370746c0000000100000000000000006a706567000000000018000003ff000000207470726c000000010000000000000000000000000017f9db00000000000000246472617400000001000000000000000000000000000000530000010000000100000000156d70736f00000001000000000000000000000000186d66726100000001000000000000000000000000000000187073667200000001000000000000000000000000000000156266726100000001000000000000000000000000166d70657300000001000000000000000000000000002868617264000000010000000000000000000000000000000000000000000000000000000000000016656e647300000001000000000000000000000000001663666c67000000010000000000000000004400000018636d66720000000100000000000000006170706c00000014636c75740000000100000000000000000000001c766572730000000100000000000000000003001c00010000"
            )
