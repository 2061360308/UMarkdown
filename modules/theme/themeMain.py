import os

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QComboBox, QFileDialog

from AppUMarkdown.application.modeIndex import moudelIndex
from tools.changeTheme import changeTheme
from .ui import Ui_Theme

from AppUMarkdown.application.extensions import appQSettings


class Theme(QWidget):
    def __init__(self, parent=None):
        super(Theme, self).__init__(parent)

        self.ui = Ui_Theme()
        self.ui.setupUi(self)

        self.setWindowTitle("主题")

        # 创建完元素再绑定信号，避免初始化数据时触发绑定信号
        self.init()

        self.ui.checkBox_2.stateChanged.connect(self.fontSwitchClicked)
        self.ui.checkBox_3.stateChanged.connect(self.bgPicSwitchClicked)
        self.ui.horizontalSlider.valueChanged.connect(self.opacitySliderChanged)
        self.ui.spinBox_2.valueChanged.connect(self.opacitySpinChanged)
        self.ui.toolButton.clicked.connect(self.toolButtonClicked)
        self.ui.comboBox.currentTextChanged.connect(self.themeComboChanged)

        self.updateTimer = QTimer()
        self.updateTimer.setInterval(300)  # 定时周期1000ms
        self.updateTimer.timeout.connect(self.updateTheme)

    def init(self):
        """
        初始化数据
        :return:
        """
        for themeName in os.listdir("res/themes"):
            self.ui.comboBox.addItem(themeName.replace(".xml", ''))

        appQSettings.beginGroup("UiTheme")
        themeNameNow = appQSettings.value("themeName")
        customFont = appQSettings.value("customFont")
        customBgPic = appQSettings.value("customBgPic")
        appQSettings.endGroup()
        self.ui.comboBox.setCurrentText(themeNameNow)
        if customFont == "false":
            self.ui.checkBox_2.setChecked(False)
            self.fontSwitchClicked(0)
        else:
            self.ui.checkBox_2.setChecked(True)
            self.fontSwitchClicked(2)

        if customBgPic == "false":
            self.ui.checkBox_3.setChecked(False)
            self.bgPicSwitchClicked(0)
        else:
            self.ui.checkBox_3.setChecked(True)
            self.bgPicSwitchClicked(2)
            appQSettings.beginGroup("customBgPic")
            path = appQSettings.value("path")
            opacity = int(float(appQSettings.value("opacity")) * 100)
            appQSettings.endGroup()

            self.ui.lineEdit.setText(path)
            self.ui.horizontalSlider.setValue(opacity)

    def fontSwitchClicked(self, state):
        """

        :param state: 0为关 2为开
        :return:
        """
        state = bool(state)

        # 判断内容是否与配置项相同，相同的话退出操作
        customFont = appQSettings.value("UiTheme/customFont")

        if (state and customFont == 'true') or ((not state) and customFont != 'true'):
            return

        self.ui.fontComboBox.setEnabled(state)
        self.ui.label_2.setEnabled(state)
        self.ui.spinBox.setEnabled(state)

    def bgPicSwitchClicked(self, state):
        state = bool(state)

        customBgPic = appQSettings.value("UiTheme/customBgPic")

        if (state and customBgPic == 'true') or ((not state) and customBgPic == 'false'):
            return

        if state:
            appQSettings.setValue("UiTheme/customBgPic", 'true')
        else:
            appQSettings.setValue("UiTheme/customBgPic", 'false')
        if state:
            nowPic = appQSettings.value("customBgPic/path")
            moudelIndex.bgImageLabel.setBg(nowPic)
        else:
            moudelIndex.bgImageLabel.setPixmap(QPixmap(""))

        connectWidgets = [
            self.ui.lineEdit,
            self.ui.label_3,
            self.ui.toolButton,
            self.ui.label_4,
            self.ui.horizontalSlider,
            self.ui.spinBox_2
        ]

        for widget in connectWidgets:
            widget.setEnabled(state)

    def opacitySliderChanged(self, value):
        """
        Slider改变
        :param value:
        :return:
        """
        opacity = int(float(appQSettings.value("customBgPic/opacity")) * 100)

        if opacity == value:
            return

        self.ui.spinBox_2.setValue(value)
        self.opacityChanged(value)

    def opacitySpinChanged(self, value):
        """
        Spin改变
        :param value:
        :return:
        """

        opacity = int(float(appQSettings.value("customBgPic/opacity")) * 100)

        if opacity == value:
            return

        self.ui.horizontalSlider.setValue(value)
        self.opacityChanged(value)

    def opacityChanged(self, opacity):
        """
        更改背景图片透明度
        :param opacity:
        :return:
        """
        appQSettings.setValue("customBgPic/opacity", opacity / 100)  # 保存设置
        if self.updateTimer.isActive():
            self.updateTimer.stop()
        self.updateTimer.start()

    def toolButtonClicked(self):
        fName, _ = QFileDialog.getOpenFileName(self, '选择图片', '.', '图像文件(*.jpg *.png)')

        path = appQSettings.value("customBgPic/path")
        if fName == path:
            return

        if fName != '':
            appQSettings.setValue("customBgPic/path", fName)
        changeTheme()

    def updateTheme(self):
        changeTheme()
        self.updateTimer.stop()

    def themeComboChanged(self, themeName):
        themeNameNow = appQSettings.value("UiTheme/themeName")

        if themeNameNow == themeName:
            return

        appQSettings.setValue('UiTheme/themeName', themeName)
        changeTheme()
