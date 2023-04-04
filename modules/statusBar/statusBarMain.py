from PySide6.QtWidgets import QStackedWidget

from modules.statusBar.ui import StatusBarUI
from AppUMarkdown.application.modeIndex import moudelIndex


class StatusBar(StatusBarUI):
    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)

        self.init()

    def init(self):
        self.tagsButton.clicked.connect(self.tagsButtonClicked)

        self.vimModeButton.clicked.connect(self.vimModeButtonClicked)
        self.readOnlyButton.clicked.connect(self.readOnlyButtonClicked)

    def tagsButtonClicked(self):
        if self.tagsButton.isChecked():
            self.tagsButton.setText(chr(0xe6f6))
            moudelIndex.stackedW.show()

            # 如果展开的面板是TocWidget那么更新他的内容
            if moudelIndex.stackedW.currentWidget() == moudelIndex.tocWidget:
                if moudelIndex.editorTabWidget.currentWidget() is not None:
                    tocHtml = moudelIndex.editorTabWidget.currentWidget().getToc()
                    moudelIndex.tocWidget.updateToc(tocHtml)
        else:
            moudelIndex.stackedW.hide()
            self.tagsButton.setText(chr(0xe6f5))

    def vimModeButtonClicked(self):
        """
        vim模式button被点击
        :return:
        """
        if self.vimModeButton.isChecked():
            moudelIndex.editorTabWidget.setVimMode(True)
        else:
            moudelIndex.editorTabWidget.setVimMode(False)

    def readOnlyButtonClicked(self):
        """
        只读模式按钮点击
        :return:
        """
        moudelIndex.editorTabWidget.updateReadOnly()

    def updateReadOnlyButton(self, on: bool):
        """
        更新只读模式按钮的状态
        :param on: 参数
        :return:
        """
        if on:
            self.readOnlyButton.setText(chr(0xe67a))
            self.readOnlyButton.setToolTip("只读模式")
        else:
            self.readOnlyButton.setText(chr(0xe678))
            self.readOnlyButton.setToolTip("写入模式")
