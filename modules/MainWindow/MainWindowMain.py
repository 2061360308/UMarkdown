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

        self.file = self.titleMenuBar.addMenu("文件(F)")
        self.file.triggered[QAction].connect(self.fileMenuClicked)
        self.fileCreate = QAction("新建", self)
        self.fileOpen = QAction("打开", self)
        self.fileSaveAs = QAction("另存为", self)
        self.fileOpenRecent = QAction("打开最近", self)
        self.fileCloseAll = QAction("关闭当前所有文件", self)
        self.fileSettings = QAction("设置", self)
        self.fileAttribute = QAction("文件属性", self)
        self.fileSaveAll = QAction("全部保存", self)
        self.fileReload = QAction("从磁盘全部重新加载", self)
        self.fileManageSettings = QAction("管理设置文件", self)
        self.fileSaveAsTemplate = QAction("将文件另存为模板", self)
        self.fileQuit = QAction("退出", self)
        self.file.addAction(self.fileCreate)
        self.file.addAction(self.fileOpen)
        self.file.addAction(self.fileSaveAs)
        self.file.addAction(self.fileOpenRecent)
        self.file.addAction(self.fileCloseAll)
        self.file.addSeparator()
        self.file.addAction(self.fileSettings)
        self.file.addAction(self.fileAttribute)
        self.file.addSeparator()
        self.file.addAction(self.fileSaveAll)
        self.file.addAction(self.fileReload)
        self.file.addSeparator()
        self.file.addAction(self.fileManageSettings)
        self.file.addAction(self.fileSaveAsTemplate)
        self.file.addSeparator()
        self.file.addAction(self.fileQuit)

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
        edit.addSeparator()
        edit.addAction(editClip)
        edit.addAction(editCopy)
        edit.addAction(editPaste)
        edit.addAction(editDelete)
        edit.addAction(editSelectAll)
        edit.addSeparator()
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
        if text == "新建":
            # 获得包含文件路径+文件名的元组
            fName, _ = QFileDialog.getSaveFileName(self, '新建文件', '.',
                                                   'Markdown文件(*.md)')
            if fName != '':
                self.editorTabWidget.openFileByInf(fName, 'UTF-8', "")

        elif text == "打开":
            fName, _ = QFileDialog.getOpenFileName(self, '打开文件', '.',
                                                   'Markdown文件(*.md *.markdown *.readme *.readMe)')
            if fName != '':
                self.editorTabWidget.openFile(fName)

    def closeEvent(self, event: QCloseEvent) -> None:
        save_state(self)
