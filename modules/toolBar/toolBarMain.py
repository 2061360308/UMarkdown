from PySide6.QtWidgets import QToolBar

from AppUMarkdown.application.modeIndex import moudelIndex
from modules.toolBar.ui import ToolBarUI


class ToolBar(ToolBarUI):
    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)

        self.previewButton.clicked.connect(self.previewButtonClicked)

    def previewButtonClicked(self):
        if self.previewButton.text() == chr(0xe64b):  # 预览模式
            self.previewButton.setText(chr(0xe64c))
            self.previewButton.setToolTip("编辑")

            moudelIndex.editorTabWidget.preview()
        else:  # 编辑模式
            self.previewButton.setToolTip("预览")
            self.previewButton.setText(chr(0xe64b))
            moudelIndex.editorTabWidget.edited()
