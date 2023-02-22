from PySide6.QtWidgets import QStackedWidget

from modules.statusBar.ui import StatusBarUI
from AppUMarkdown.application.modeIndex import moudelIndex


class StatusBar(StatusBarUI):
    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)

        self.init()

    def init(self):
        self.tagsButton.clicked.connect(self.tagsButtonClicked)

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