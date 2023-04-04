import json

from PySide6.QtCore import Qt, QUrl, QObject, Signal, Slot
from PySide6.QtGui import QColor
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

from AppUMarkdown.application.modeIndex import moudelIndex
from AppUMarkdown import appQSettings


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
        if appQSettings.value("MainWindowState/vimMode") == "true":
            self.parent().setVimMode(moudelIndex.mainWindow.statusBarW.vimModeButton.isChecked())

    @Slot(str)
    def contentChange(self, content):
        # print("内容改变事件被触发")
        self.parent().contentChangeSignal.emit(content)

    @Slot(str)
    def historySizeChange(self, data):
        undo_num, redo_num = json.loads(data)
        if undo_num == 0:
            moudelIndex.mainWindow.editUndo.setEnabled(False)
            moudelIndex.mainWindow.editSelectUndo.setEnabled(False)
        else:
            moudelIndex.mainWindow.editUndo.setEnabled(True)
            moudelIndex.mainWindow.editSelectUndo.setEnabled(True)

        if redo_num == 0:
            moudelIndex.mainWindow.editRedo.setEnabled(False)
            moudelIndex.mainWindow.editSelectRedo.setEnabled(False)
        else:
            moudelIndex.mainWindow.editRedo.setEnabled(True)
            moudelIndex.mainWindow.editSelectRedo.setEnabled(True)

    @Slot(str)
    def selectionsChange(self, jsonData):
        selections = json.loads(jsonData)
        self.parent().selectionsChangeSignal.emit(selections)


class CodemirrorWidget(QWebEngineView):
    """ Codemirror编辑框 """

    contentChangeSignal = Signal(str)
    selectionsChangeSignal = Signal(list)

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

    def execCommand(self, command):
        """
        执行命令
        :param command:
        :return:
        """
        self.JsBridge.runJavascript("execCommand", command)

    def clearSelectionContent(self):
        self.JsBridge.runJavascript("replaceSelection", '')

    def changeSelectionContent(self, n_text: str):
        self.JsBridge.runJavascript("replaceSelection", n_text)

    def insertContent(self, content):
        self.JsBridge.runJavascript("insertContent", content)

    def setVimMode(self, p: bool):
        if p:
            self.JsBridge.runJavascript("changeKeyMap", "vim")
        else:
            self.JsBridge.runJavascript("changeKeyMap", "default")

    def setReadOnly(self, on: bool):
        self.JsBridge.runJavascript("setReadOnly", on)
