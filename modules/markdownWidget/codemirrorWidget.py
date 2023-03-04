import json

from PySide6.QtCore import Qt, QUrl, QObject, Signal, Slot
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

        self.init_connect = self.parent().init_content
        self.page = self.parent().page()
        self.loadFinishSign = self.parent().loadFinishSign
        self.initLoad = self.parent().initLoad

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
        if self.parent().initLoad:
            self.runJavascript("setContent", self.parent().getContent())

    @Slot(str)
    def contentChange(self, content):
        # print("内容改变事件被触发")
        self.parent().contentChangeSignal.emit(content)


class CodemirrorWidget(QWebEngineView):
    """ Codemirror编辑框 """

    contentChangeSignal = Signal(str)

    loadFinishSign = False
    initLoad = False

    def __init__(self, parent=None, init_connect=""):
        super(CodemirrorWidget, self).__init__(parent)

        self.init_content = init_connect

        # 配置浏览器
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, True)
        self.page().setBackgroundColor(QColor(0, 0, 0, 0))
        self.setUrl(QUrl("file:///%s" % "codemirror/CodemirrorWidget.html"))
        channel = QWebChannel(self.page())
        self.page().setWebChannel(channel)
        self.JsBridge = Bridge(self)
        channel.registerObject("Bridge", self.JsBridge)  # 注册，js通过pythonBridge调用

    def updateTheme(self):
        self.JsBridge.runJavascript("updateTheme", None)

    def getContent(self):
        return self.parent().fileContent

    def loadFile(self):
        """
        打开文件
        :param content:
        :param path:
        :return:
        """
        if self.loadFinishSign:
            self.JsBridge.runJavascript("setContent", self.getContent())
        else:
            # 编辑器没加载完，记录下任务
            self.initLoad = True
