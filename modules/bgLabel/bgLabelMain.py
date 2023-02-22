from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel

from AppUMarkdown import appQSettings


class BgLabel(QLabel):
    def __init__(self, parent=None):
        super(BgLabel, self).__init__(parent)

        self.bgPath = None
        self.parent().installEventFilter(self)

    def setBg(self, path):
        self.bgPath = path
        customBgPic = appQSettings.value('UiTheme/customBgPic')
        if customBgPic != "false":
            pixmap = QPixmap(self.bgPath).scaled(self.parent().size(), aspectMode=Qt.KeepAspectRatioByExpanding)
            self.setPixmap(pixmap)
            self.repaint()
        else:
            self.setPixmap(QPixmap(""))

    def eventFilter(self, widget, event):
        try:
            customBgPic = appQSettings.value('UiTheme/customBgPic')
        except:
            return False
        if event.type() == QtCore.QEvent.Type.Resize:  # 判断事件类型
            self.resize(event.size())
            if customBgPic != "false":
                pixmap = QPixmap(self.bgPath).scaled(event.size(), aspectMode=Qt.KeepAspectRatioByExpanding)
                self.setPixmap(pixmap)

        return False
