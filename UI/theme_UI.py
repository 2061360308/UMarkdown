# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'theme.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFontComboBox,
                               QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                               QSizePolicy, QSlider, QSpacerItem, QSpinBox,
                               QToolButton, QVBoxLayout)


class Ui_Theme(object):
    def setupUi(self, Theme):
        if not Theme.objectName():
            Theme.setObjectName(u"Theme")
        Theme.resize(574, 496)
        self.verticalLayout = QVBoxLayout(Theme)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Theme)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBox = QComboBox(Theme)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.checkBox = QCheckBox(Theme)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout.addWidget(self.checkBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_2 = QCheckBox(Theme)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_2.addWidget(self.checkBox_2)

        self.fontComboBox = QFontComboBox(Theme)
        self.fontComboBox.setObjectName(u"fontComboBox")

        self.horizontalLayout_2.addWidget(self.fontComboBox)

        self.horizontalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.label_2 = QLabel(Theme)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.spinBox = QSpinBox(Theme)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(8)
        self.spinBox.setMaximum(72)
        self.spinBox.setValue(12)

        self.horizontalLayout_2.addWidget(self.spinBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.groupBox = QGroupBox(Theme)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkBox_3 = QCheckBox(self.groupBox)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.verticalLayout_2.addWidget(self.checkBox_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.toolButton = QToolButton(self.groupBox)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout_3.addWidget(self.toolButton)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.horizontalSlider = QSlider(self.groupBox)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(15)
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.horizontalSlider)

        self.spinBox_2 = QSpinBox(self.groupBox)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setMaximum(100)
        self.spinBox_2.setValue(15)

        self.horizontalLayout_4.addWidget(self.spinBox_2)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.label_5)

        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.retranslateUi(Theme)

        QMetaObject.connectSlotsByName(Theme)

    # setupUi

    def retranslateUi(self, Theme):
        Theme.setWindowTitle(QCoreApplication.translate("Theme", u"Form", None))
        self.label.setText(QCoreApplication.translate("Theme", u"\u4e3b\u9898", None))
        self.checkBox.setText(QCoreApplication.translate("Theme", u"\u4e0e\u64cd\u4f5c\u7cfb\u7edf\u540c\u6b65", None))
        self.checkBox_2.setText(
            QCoreApplication.translate("Theme", u"\u4f7f\u7528\u81ea\u5b9a\u4e49\u5b57\u4f53", None))
        self.label_2.setText(QCoreApplication.translate("Theme", u"\u5927\u5c0f", None))
        self.groupBox.setTitle(QCoreApplication.translate("Theme", u"\u80cc\u666f\u56fe\u50cf", None))
        self.checkBox_3.setText(QCoreApplication.translate("Theme", u"\u542f\u7528\u80cc\u666f\u56fe\u50cf", None))
        self.label_3.setText(QCoreApplication.translate("Theme", u"\u56fe\u50cf", None))
        self.toolButton.setText(QCoreApplication.translate("Theme", u"...", None))
        self.label_4.setText(QCoreApplication.translate("Theme", u"\u4e0d\u900f\u660e\u5ea6", None))
        self.label_5.setText("")
    # retranslateUi
