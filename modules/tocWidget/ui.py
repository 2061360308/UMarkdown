from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView


class TocWidgetUI(QWebEngineView):
    def __init__(self, parent):
        super(TocWidgetUI, self).__init__(parent)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, True)  # 启用滚动条
        self.page().settings().setAttribute(QWebEngineSettings.AutoLoadIconsForPage, False)  # 不自动下载网页图标
        self.page().setBackgroundColor(QColor(0, 0, 0, 0))
        self.setUrl(QUrl("file:///%s" % "codemirror/TocWidget.html"))
