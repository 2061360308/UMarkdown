from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QAction, QIcon, QCloseEvent, QKeySequence
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
        self.fileCreate.setShortcut(QKeySequence.New)
        self.fileOpen = QAction("打开", self)
        self.fileOpen.setShortcut(QKeySequence.Open)
        self.fileSave = QAction("保存", self)
        self.fileSave.setShortcut(QKeySequence.Save)
        self.fileSaveAs = QAction("另存为", self)
        self.fileOpenRecent = QAction("打开最近(待开发)", self)
        self.fileCloseAll = QAction("关闭当前所有文件", self)
        self.fileSettings = QAction("设置(待开发)", self)
        self.fileAttribute = QAction("文件属性(待开发)", self)
        self.fileSaveAll = QAction("全部保存(待开发)", self)
        self.fileReload = QAction("从磁盘全部重新加载(待开发)", self)
        self.fileManageSettings = QAction("管理设置文件(待开发)", self)
        self.fileSaveAsTemplate = QAction("将文件另存为模板(待开发)", self)
        self.fileQuit = QAction("退出", self)
        self.file.addAction(self.fileCreate)
        self.file.addAction(self.fileOpen)
        self.file.addAction(self.fileSave)
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

        self.edit = self.titleMenuBar.addMenu("编辑(E)")
        self.edit.triggered[QAction].connect(self.editMenuClicked)
        self.editInsertMenu = self.edit.addMenu("插入")
        self.editInsertTitle = QAction("标题")
        self.editInsertPicture = QAction("图片")
        self.editInsertLink = QAction("链接")
        self.editInsertCode = QAction("代码段")
        self.editInsertQuote = QAction("引用")
        self.editInsertTodo = QAction("待办列表")
        self.editInsertOrder = QAction("有序列表")
        self.editInsertUnorder = QAction("无序列表")
        self.editInsertMenu.addAction(self.editInsertTitle)
        self.editInsertMenu.addAction(self.editInsertPicture)
        self.editInsertMenu.addAction(self.editInsertLink)
        self.editInsertMenu.addAction(self.editInsertCode)
        self.editInsertMenu.addAction(self.editInsertQuote)
        self.editInsertMenu.addAction(self.editInsertTodo)
        self.editInsertMenu.addAction(self.editInsertOrder)
        self.editInsertMenu.addAction(self.editInsertUnorder)
        # self.edit.
        self.editUndo = QAction("撤销", self)
        self.editUndo.setEnabled(False)
        self.editUndo.setShortcut(QKeySequence.Undo)
        self.editRedo = QAction("重做", self)
        self.editRedo.setEnabled(False)
        self.editRedo.setShortcut(QKeySequence.Redo)
        self.editSelectUndo = QAction("撤销选择", self)
        self.editSelectUndo.setEnabled(False)
        self.editSelectRedo = QAction("重做选择", self)
        self.editSelectRedo.setEnabled(False)
        self.editClip = QAction("剪贴", self)
        self.editClip.setEnabled(False)
        self.editClip.setShortcut(QKeySequence.Cut)
        self.editCopy = QAction("复制", self)
        self.editCopy.setEnabled(False)
        self.editCopy.setShortcut(QKeySequence.Copy)
        self.editPaste = QAction("粘贴", self)
        self.editPaste.setShortcut(QKeySequence.Paste)
        self.editDelete = QAction("删除", self)
        self.editDelete.setEnabled(False)
        self.editDelete.setShortcut(QKeySequence.Delete)
        self.editSelectAll = QAction("全选", self)
        self.editSelectAll.setShortcut(QKeySequence.SelectAll)
        self.editFind = QAction("查找", self)
        self.editFind.setShortcut(QKeySequence.Find)
        self.editReplace = QAction("替换", self)
        self.editReplace.setShortcut(QKeySequence.Replace)
        # self.edit.addAction(self.editAdd)
        self.edit.addAction(self.editUndo)
        self.edit.addAction(self.editRedo)
        self.edit.addAction(self.editSelectUndo)
        self.edit.addAction(self.editSelectRedo)
        self.edit.addSeparator()
        self.edit.addAction(self.editClip)
        self.edit.addAction(self.editCopy)
        self.edit.addAction(self.editPaste)
        self.edit.addAction(self.editDelete)
        self.edit.addAction(self.editSelectAll)
        self.edit.addSeparator()
        self.edit.addAction(self.editFind)
        self.edit.addAction(self.editReplace)

        self.titleMenuBar.addMenu("工具(T)")

        theme = self.titleMenuBar.addMenu("主题(S)")
        theme.triggered[QAction].connect(self.themeClicked)
        themeUI = QAction("界面主题", self)
        themePreview = QAction("预览主题", self)
        theme.addAction(themeUI)
        theme.addAction(themePreview)

        self.help = self.titleMenuBar.addMenu("帮助(H)")
        self.helpGithub = QAction("UMarkdown Github主页")
        self.helpAuthorCSDN = QAction("作者的CSDN主页")
        self.helpAuthorBlog = QAction("作者的Blog小站")
        self.help.addAction(self.helpGithub)
        self.help.addAction(self.helpAuthorCSDN)
        self.help.addAction(self.helpAuthorBlog)

        self.tocWidget.tocClickedSignal.connect(self.tocTitleClicked)

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
        elif text == "另存为":
            self.editorTabWidget.saveFileAs()
        elif text == "关闭当前所有文件":
            self.editorTabWidget.closeAll()
        elif text == "退出":
            self.close()
        elif text == "保存":
            self.editorTabWidget.saveFile()

    def editMenuClicked(self, action: QAction):
        text = action.text()
        if text == "撤销":
            self.editorTabWidget.currentWidget().commandUndo()
        elif text == "重做":
            self.editorTabWidget.currentWidget().commandRedo()
        elif text == "撤销选择":
            self.editorTabWidget.currentWidget().commandUndoSelection()
        elif text == "重做选择":
            self.editorTabWidget.currentWidget().commandRedoSelection()
        elif text == "剪贴":
            self.editorTabWidget.currentWidget().clipSelections()
        elif text == "复制":
            self.editorTabWidget.currentWidget().copySelections()
        elif text == "粘贴":
            self.editorTabWidget.currentWidget().paste()
        elif text == "删除":
            self.editorTabWidget.currentWidget().deleteSelections()
        elif text == "全选":
            self.editorTabWidget.currentWidget().commandSelectAll()
        elif text == "查找":
            self.editorTabWidget.currentWidget().commandFind()
        elif text == "替换":
            self.editorTabWidget.currentWidget().commandReplace()
        elif text == "标题":
            widget = self.editorTabWidget.currentWidget()
            if widget.selections:
                selection = widget.selections[0]

                if selection.startswith("# "):
                    widget.changeSelectionContent(selection[2:])
                else:
                    widget.changeSelectionContent("# " + selection)
            else:
                widget.insertContent("# ")
        elif text == "图片":
            widget = self.editorTabWidget.currentWidget()
            if widget.selections:
                selection = widget.selections[0]

                widget.changeSelectionContent("![" + selection+"]()")
            else:
                widget.insertContent("![]()")
        elif text == "链接":
            widget = self.editorTabWidget.currentWidget()
            if widget.selections:
                selection = widget.selections[0]

                widget.changeSelectionContent("[" + selection + "]()")
            else:
                widget.insertContent("[]()")
        elif text == "代码段":
            widget = self.editorTabWidget.currentWidget()
            if widget.selections:
                selection = widget.selections[0]

                widget.changeSelectionContent("```\n" + selection + "\n```")
            else:
                widget.insertContent("```\n```")
        elif text == "引用":
            widget = self.editorTabWidget.currentWidget()
            if widget.selections:
                selection = widget.selections[0]

                if selection.startswith("> "):
                    widget.changeSelectionContent(selection[2:])
                else:
                    widget.changeSelectionContent("> " + selection)
            else:
                widget.insertContent("> ")
        elif text == "待办列表":
            widget = self.editorTabWidget.currentWidget()
            if widget.selections:
                selection = widget.selections[0]

                itemList = selection.split("\n")

                # 判断是否是标准形式

                standFormat = True

                for i in itemList:
                    if i.startswith("- [ ] ") or i.startswith("- [x] "):
                        continue
                    else:
                        standFormat = False
                        break

                n_text = ""

                if standFormat:  # 是标准型，给他恢复为普通文本
                    for i in itemList:
                        n_text = n_text + i[6:] + "\n"
                else:  # 不是标准型，更改为标准格式
                    for i in itemList:
                        if i.startswith("- [ ] ") or i.startswith("- [x] "):
                            n_text = n_text + i + "\n"
                        else:
                            n_text = n_text + "- [ ] " + i + "\n"

                widget.changeSelectionContent(n_text[:-1])
            else:
                widget.insertContent("- [ ] ")

        elif text == "无序列表":
            widget = self.editorTabWidget.currentWidget()
            if widget.selections:
                selection = widget.selections[0]

                itemList = selection.split("\n")

                # 判断是否是标准形式

                standFormat = True

                for i in itemList:
                    if i.startswith("- "):
                        continue
                    else:
                        standFormat = False
                        break

                n_text = ""

                if standFormat:  # 是标准型，给他恢复为普通文本
                    for i in itemList:
                        n_text = n_text + i[2:] + "\n"
                else:  # 不是标准型，更改为标准格式
                    for i in itemList:
                        if i.startswith("- "):
                            n_text = n_text + i + "\n"
                        else:
                            n_text = n_text + "- " + i + "\n"

                widget.changeSelectionContent(n_text[:-1])
            else:
                widget.insertContent("- ")
        elif text == "有序列表":
            widget = self.editorTabWidget.currentWidget()
            if widget.selections:
                selection = widget.selections[0]

                itemList = selection.split("\n")

                # 判断是否是标准形式

                standFormat = True

                j = 0
                for i in itemList:
                    j = j + 1
                    if i.startswith("%s. " % j):
                        continue
                    else:
                        standFormat = False
                        break

                n_text = ""

                if standFormat:  # 是标准型，给他恢复为普通文本
                    for i in itemList:
                        n_text = n_text + i[3:] + "\n"
                else:  # 不是标准型，更改为标准格式
                    j = 0
                    for i in itemList:
                        j = j + 1
                        if i.startswith("%s. " % j):
                            n_text = n_text + i + "\n"
                        else:
                            n_text = n_text + "%s. " % j + i + "\n"

                widget.changeSelectionContent(n_text[:-1])
            else:
                widget.insertContent("1. ")


    def tocTitleClicked(self, href):
        self.editorTabWidget.currentWidget().skipTitle(href)

    def closeEvent(self, event: QCloseEvent) -> None:
        save_state(self)
