import json

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWebChannel import QWebChannel

from .ui import TocWidgetUI


class Bridge(QObject):
    """
    python 和 Js 桥梁
    """

    def __init__(self, parent):
        super(Bridge, self).__init__(parent)

        self.page = self.parent().page()

    def runJavascript(self, fun, data, js_callback=None):
        if not isinstance(data, dict):
            data = {"data": data}
        if js_callback is None:
            self.page.runJavaScript("%s(%s)" % (fun, json.dumps(data)))
        else:
            self.page.runJavaScript("%s(%s)" % (fun, json.dumps(data)), 0, js_callback)

    @Slot(str)
    def titleClicked(self, href):
        href = href.replace('file:///codemirror/TocWidget.html', '')
        self.parent().tocClickedSignal.emit(href)


class TocWidget(TocWidgetUI):

    tocClickedSignal = Signal(str)
    def __init__(self, parent):
        super(TocWidget, self).__init__(parent)

        channel = QWebChannel(self.page())
        self.page().setWebChannel(channel)
        self.JsBridge = Bridge(self)
        channel.registerObject("Bridge", self.JsBridge)  # 注册，js通过pythonBridge调用

    def updateToc(self, tocHtml: str):
        self.JsBridge.runJavascript("updateToc", tocHtml)
