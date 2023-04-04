import json

from PySide6.QtCore import QUrl, Qt, QObject, Signal, Slot
from PySide6.QtGui import QColor
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

from AppUMarkdown import appQSettings


class Bridge(QObject):
    """
    python 和 Js 桥梁
    """

    def __init__(self, parent):
        super(Bridge, self).__init__(parent)

        self.filePath = "aaaaaa"

        self.page = self.parent().page()

    def runJavascript(self, fun, data, js_callback=None):
        if not isinstance(data, dict):
            data = {"data": data}
        if js_callback is None:
            self.page.runJavaScript("%s(%s)" % (fun, json.dumps(data)))
        else:
            self.page.runJavaScript("%s(%s)" % (fun, json.dumps(data)), 0, js_callback)


    @Slot()
    def loadFinish(self):
        """
        加载完毕事件
        :return:
        """
        self.parent().loadFinishSign = True

        self.runJavascript("setFilePath", self.parent().filePath)

        # 如果有之前的任务，那么加载
        if self.parent().task:
            self.runJavascript("prase", self.parent().task, self.parent().praseHtmlCallBack)
            self.parent().task = None

        oldPreviewTheme = appQSettings.value("PreviewTheme")
        previewTheme = appQSettings.value("PreviewTheme")
        if previewTheme is not None:
            """
            res/previewThems\\Vintage\\typora-vintage-theme-master\\vintage_night.css
            """
            name = "editor/css/previewTheme/" + previewTheme.split("\\")[-1]
            self.parent().updatePreviewTheme("editor/css/dark.css", name)


class PreviewWidget(QWebEngineView):
    """ 预览框 """

    tocUpdateSignal = Signal(str)

    loadFinishSign = False
    task = None
    tocHtml = None
    previewHtml = None

    def __init__(self, parent):
        super(PreviewWidget, self).__init__(parent)

        # 配置浏览器
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, True)  # 启用滚动条
        self.page().settings().setAttribute(QWebEngineSettings.AutoLoadIconsForPage, False)  # 不自动下载网页图标
        self.page().settings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent,
                                            True)  # run JavaScript, CSS, plugins or web-sockets from HTTP URLs.
        self.page().settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)  # 允许本地url访问外部url
        self.page().setBackgroundColor(QColor(0, 0, 0, 0))
        self.setUrl(QUrl("file:///%s" % "codemirror/PreviewWidget.html"))
        # self.setUrl(QUrl("file:///%s" % "codemirror/MarkdownEditor.html"))
        channel = QWebChannel(self.page())
        self.page().setWebChannel(channel)
        self.JsBridge = Bridge(self)

        channel.registerObject("Bridge", self.JsBridge)  # 注册，js通过pythonBridge调用

    def setFilePath(self, filePath):
        """
                设置文件路径
                :param path:
                :return:
                """
        self.filePath = filePath


    def praseHtml(self, content):
        # 先判断当前组件是否加载完毕，没有的话将这个任务暂时记录下来
        if self.loadFinishSign:
            self.JsBridge.runJavascript("prase", content, self.praseHtmlCallBack)
        else:
            self.task = content

    def praseHtmlCallBack(self, tocHtml):
        """
        解析的回调，返回了toc目录
        :param tocHtml:
        :return:
        """
        self.tocHtml = json.loads(tocHtml)['toc']
        self.previewHtml = json.loads(tocHtml)['previewHtml']
        self.tocUpdateSignal.emit(self.tocHtml)

    def updatePreviewTheme(self, old, new):
        self.JsBridge.runJavascript("updatePreviewTheme", [old, new])

    def skipTitle(self, href):
        self.JsBridge.runJavascript("skipTitle", href)
