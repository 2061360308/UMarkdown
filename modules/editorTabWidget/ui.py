from PySide6.QtWidgets import QTabWidget

from modules.markdownWidget.markdownWidgetMain import MarkdownWidget


class EditorTabWidgetUI(QTabWidget):
    def __init__(self, parent=None):
        super(EditorTabWidgetUI, self).__init__(parent)

        # self.setStyleSheet("background-color:rgba(0,0,0,0)")
        self.setDocumentMode(True)
        self.setTabsClosable(True)
        self.setMovable(True)

    def init(self):
        pass
