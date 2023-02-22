from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QAction, QIcon, QCloseEvent
from PySide6.QtWidgets import QMenu, QFileDialog

from AppUMarkdown.app_fun.windows_state import save_state, load_state
from AppUMarkdown.application.extensions import appQSettings

from res import resources  # type: ignore

from .ui import MainWindowUI
from ..theme.themeMain import Theme


class MainWindow(MainWindowUI):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init()

        load_state(self)

    def init(self):
        icon = self.titleMenuBar.addMenu("")
        icon.setIcon(QIcon(":/icons/UMarkdownIcon_png"))

        file = self.titleMenuBar.addMenu("文件(F)")
        file.triggered[QAction].connect(self.fileMenuClicked)
        fileCreate = QAction("新建", self)
        fileOpen = QAction("打开", self)
        fileSaveAs = QAction("另存为", self)
        fileOpenRecent = QAction("打开最近", self)
        fileCloseAll = QAction("关闭当前所有文件", self)
        fileSettings = QAction("设置", self)
        fileAttribute = QAction("文件属性", self)
        fileSaveAll = QAction("全部保存", self)
        fileReload = QAction("从磁盘全部重新加载", self)
        fileManageSettings = QAction("管理设置文件", self)
        fileSaveAsTemplate = QAction("将文件另存为模板", self)
        fileQuit = QAction("退出", self)
        file.addAction(fileCreate)
        file.addAction(fileOpen)
        file.addAction(fileSaveAs)
        file.addAction(fileOpenRecent)
        file.addAction(fileCloseAll)
        file.addSeparator()
        file.addAction(fileSettings)
        file.addAction(fileAttribute)
        file.addSeparator()
        file.addAction(fileSaveAll)
        file.addAction(fileReload)
        file.addSeparator()
        file.addAction(fileManageSettings)
        file.addAction(fileSaveAsTemplate)
        file.addSeparator()
        file.addAction(fileQuit)

        edit = self.titleMenuBar.addMenu("编辑(E)")
        editUpdo = QAction("撤销", self)
        editRedo = QAction("重做", self)
        editClip = QAction("剪贴", self)
        editCopy = QAction("复制", self)
        editPaste = QAction("粘贴", self)
        editDelete = QAction("删除", self)
        editSelectAll = QAction("全选", self)
        editFind = QAction("查找", self)
        editReplace = QAction("替换", self)
        edit.addAction(editUpdo)
        edit.addAction(editRedo)
        file.addSeparator()
        edit.addAction(editClip)
        edit.addAction(editCopy)
        edit.addAction(editPaste)
        edit.addAction(editDelete)
        edit.addAction(editSelectAll)
        file.addSeparator()
        edit.addAction(editFind)
        edit.addAction(editReplace)


        self.titleMenuBar.addMenu("工具(T)")

        theme = self.titleMenuBar.addMenu("主题(S)")
        theme.triggered[QAction].connect(self.themeClicked)
        themeUI = QAction("界面主题", self)
        themePreview = QAction("预览主题", self)
        theme.addAction(themeUI)
        theme.addAction(themePreview)

        self.titleMenuBar.addMenu("帮助(H)")

    def themeClicked(self, action: QAction):
        text = action.text()
        if text == "界面主题":
            self.themeW = Theme()
            self.themeW.show()
        elif text == "预览主题":
            pass

    def fileMenuClicked(self, action: QAction):
        text = action.text()

        if text == "打开":
            fName, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', 'Markdown文件(*.md *.markdown *.readme *.readMe)')
            if fName != '':
                self.editorTabWidget.openFile(fName)

    def closeEvent(self, event: QCloseEvent) -> None:
        save_state(self)