# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from tank.platform.qt import QtCore
for name, cls in QtCore.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls

from tank.platform.qt import QtGui
for name, cls in QtGui.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls


from ..qtwidgets import ContextWidget

from  . import resources_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(495, 430)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stack_widget = QStackedWidget(Dialog)
        self.stack_widget.setObjectName(u"stack_widget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout = QVBoxLayout(self.page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.version_name_label = QLabel(self.page)
        self.version_name_label.setObjectName(u"version_name_label")

        self.horizontalLayout.addWidget(self.version_name_label)

        self.version_name = QLineEdit(self.page)
        self.version_name.setObjectName(u"version_name")

        self.horizontalLayout.addWidget(self.version_name)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.context_widget = ContextWidget(self.page)
        self.context_widget.setObjectName(u"context_widget")

        self.verticalLayout.addWidget(self.context_widget)

        self.spacer_label = QLabel(self.page)
        self.spacer_label.setObjectName(u"spacer_label")

        self.verticalLayout.addWidget(self.spacer_label)

        self.description_label = QLabel(self.page)
        self.description_label.setObjectName(u"description_label")

        self.verticalLayout.addWidget(self.description_label)

        self.description = QTextEdit(self.page)
        self.description.setObjectName(u"description")

        self.verticalLayout.addWidget(self.description)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.frame_range = QLabel(self.page)
        self.frame_range.setObjectName(u"frame_range")

        self.horizontalLayout_5.addWidget(self.frame_range)

        self.start_frame = QLineEdit(self.page)
        self.start_frame.setObjectName(u"start_frame")
        self.start_frame.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_5.addWidget(self.start_frame)

        self.frame_range_to = QLabel(self.page)
        self.frame_range_to.setObjectName(u"frame_range_to")

        self.horizontalLayout_5.addWidget(self.frame_range_to)

        self.end_frame = QLineEdit(self.page)
        self.end_frame.setObjectName(u"end_frame")
        self.end_frame.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_5.addWidget(self.end_frame)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.playlists = QComboBox(self.page)
        self.playlists.setObjectName(u"playlists")

        self.horizontalLayout_5.addWidget(self.playlists)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.stack_widget.addWidget(self.page)
        self.description.raise_()
        self.description_label.raise_()
        self.context_widget.raise_()
        self.spacer_label.raise_()
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout = QGridLayout(self.page_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 41, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_6 = QLabel(self.page_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(100, 100))
        self.label_6.setMaximumSize(QSize(100, 100))
        self.label_6.setPixmap(QPixmap(u":/tk_nuke_quickreview/complete.png"))
        self.label_6.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.label_6)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.label_8 = QLabel(self.page_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse)

        self.verticalLayout_3.addWidget(self.label_8)

        self.jump_to_shotgun = QPushButton(self.page_2)
        self.jump_to_shotgun.setObjectName(u"jump_to_shotgun")

        self.verticalLayout_3.addWidget(self.jump_to_shotgun)

        self.jump_to_panel = QPushButton(self.page_2)
        self.jump_to_panel.setObjectName(u"jump_to_panel")

        self.verticalLayout_3.addWidget(self.jump_to_panel)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(31, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 1, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.stack_widget.addWidget(self.page_2)

        self.verticalLayout_2.addWidget(self.stack_widget)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(148, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.cancel = QPushButton(Dialog)
        self.cancel.setObjectName(u"cancel")

        self.horizontalLayout_2.addWidget(self.cancel)

        self.submit = QPushButton(Dialog)
        self.submit.setObjectName(u"submit")

        self.horizontalLayout_2.addWidget(self.submit)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        QWidget.setTabOrder(self.description, self.version_name)
        QWidget.setTabOrder(self.version_name, self.start_frame)
        QWidget.setTabOrder(self.start_frame, self.end_frame)
        QWidget.setTabOrder(self.end_frame, self.submit)
        QWidget.setTabOrder(self.submit, self.cancel)
        QWidget.setTabOrder(self.cancel, self.jump_to_panel)

        self.retranslateUi(Dialog)

        self.stack_widget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Flow Production Tracking Publish", None))
        self.version_name_label.setText(QCoreApplication.translate("Dialog", u"Name:", None))
        self.spacer_label.setText("")
        self.description_label.setText(QCoreApplication.translate("Dialog", u"Description:", None))
        self.frame_range.setText(QCoreApplication.translate("Dialog", u"Frame Range:", None))
        self.frame_range_to.setText(QCoreApplication.translate("Dialog", u"to", None))
        self.label_6.setText("")
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Version Creation Complete!", None))
        self.jump_to_shotgun.setText(QCoreApplication.translate("Dialog", u"Show in Flow Production Tracking", None))
        self.jump_to_panel.setText(QCoreApplication.translate("Dialog", u"Show in Panel", None))
        self.cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.submit.setText(QCoreApplication.translate("Dialog", u"Upload to Flow Production Tracking", None))
    # retranslateUi

Error: C:\Users\chaucae\Documents\projects\tk-nuke-quickreview\resources\dialog.ui: Warning: Z-order assignment: '' is not a valid widget.

while executing 'c:\users\chaucae\documents\projects\tk-core\.venv\lib\site-packages\PySide2\uic -g python -g python --from-imports C:\Users\chaucae\Documents\projects\tk-nuke-quickreview\resources/dialog.ui'
