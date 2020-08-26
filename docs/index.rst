Shotgun Nuke Quickreview API reference, |release|
###################################################


The ``tk-nuke-quickreview`` app adds a custom gizmo to the shotgun node menu in Nuke.

Via a user interface, the user can create a Shotgun ``Version``.

The following items are configurable via the UI:

- The name of the Version.
- The entity link and task that should be associated with the Version.
- Description.
- Frame range to submit.
- Whether to add the created Version to a playlist.

During the submission process several things happen:

- A quicktime file with slates and burnins is rendered out by Nuke
- A Shotgun Version entity is created
- The quicktime is uploaded to Shotgun and deleted from disk.

Several aspects of the process are customizable via the following Hooks:

.. py:currentmodule:: tk_nuke_quickreview.base_hooks

Controlling naming and formatting
---------------------------------

.. autoclass:: ReviewSettings
    :members:


Adding events and automation
----------------------------

.. autoclass:: ReviewEvents
    :members:
