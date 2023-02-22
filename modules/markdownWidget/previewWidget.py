import json

from PySide6.QtCore import QUrl, Qt, QObject, Signal
from PySide6.QtGui import QColor
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView


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


class PreviewWidget(QWebEngineView):
    """ 预览框 """

    tocUpdateSignal = Signal(str)

    def __init__(self, parent):
        super(PreviewWidget, self).__init__(parent)

        # 配置浏览器
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, True)  # 启用滚动条
        self.page().settings().setAttribute(QWebEngineSettings.AutoLoadIconsForPage, False)  # 不自动下载网页图标
        self.page().setBackgroundColor(QColor(0, 0, 0, 0))
        self.setUrl(QUrl("file:///%s" % "codemirror/PreviewWidget.html"))
        # self.setUrl(QUrl("file:///%s" % "codemirror/MarkdownEditor.html"))
        channel = QWebChannel(self.page())
        self.page().setWebChannel(channel)
        self.JsBridge = Bridge(self)
        channel.registerObject("Bridge", self.JsBridge)  # 注册，js通过pythonBridge调用

    def praseHtml(self, content):
        self.JsBridge.runJavascript("prase", content, self.praseHtmlCallBack)

    def praseHtmlCallBack(self, tocHtml):
        """
        解析的回调，返回了toc目录
        :param tocHtml:
        :return:
        """
        self.tocUpdateSignal.emit(json.loads(tocHtml)['data'])
