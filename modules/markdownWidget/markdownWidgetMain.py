import os.path

from PySide6.QtWidgets import QFileDialog

import pyperclip

from AppUMarkdown.application.modeIndex import moudelIndex
from .ui import MarkdownWidgetUI


class MarkdownWidget(MarkdownWidgetUI):
    # 属性
    fileName = None  # 文件名
    filePath = None  # 文件路径
    fileEncoding = None  # 文件编码
    fileContent = None  # 文件内容
    openEncoding = None  # 打开文件所用的编码

    fileToc = None  # 文章目录

    changeMark = None  # 改动标识

    def __init__(self, parent=None):
        super(MarkdownWidget, self).__init__(parent)

        self.selections = []

        self.codemirrorWidget.contentChangeSignal.connect(self.connectChange)
        self.codemirrorWidget.selectionsChangeSignal.connect(self.selectionsChange)
        self.previewWidget.tocUpdateSignal.connect(self.tocUpdate)

    def initFile(self, **kwargs):
        self.fileName = kwargs.get("fileName")
        self.filePath = kwargs.get("filePath")
        self.fileEncoding = kwargs.get("fileEncoding")
        self.fileContent = kwargs.get("fileContent")
        self.openEncoding = kwargs.get("openEncoding")

        self.codemirrorWidget.loadFile()

    def connectChange(self, content):
        self.previewWidget.praseHtml(content)
        self.fileContent = content

    def selectionsChange(self, selections):
        if selections == ['']:
            selections = []
            moudelIndex.mainWindow.editClip.setEnabled(False)
            moudelIndex.mainWindow.editCopy.setEnabled(False)
            moudelIndex.mainWindow.editDelete.setEnabled(False)
        else:
            moudelIndex.mainWindow.editClip.setEnabled(True)
            moudelIndex.mainWindow.editCopy.setEnabled(True)
            moudelIndex.mainWindow.editDelete.setEnabled(True)
        self.selections = selections

    def tocUpdate(self, tocHtml):
        # 更新文章的toc属性
        self.fileToc = tocHtml

        # 如果statusBarW的TocWidget处于打开状态那么更新他的内容
        tocOpen = moudelIndex.statusBarW.tagsButton.isChecked()
        if tocOpen:
            moudelIndex.tocWidget.updateToc(tocHtml)

    def getToc(self):
        return self.fileToc

    def updateTheme(self):
        self.codemirrorWidget.updateTheme()

    def saveFile(self) -> bool:
        filePath = self.filePath
        # fileEncoding = widget.fileEncoding
        # fileContent = widget.fileContent
        if self.filePath is None:
            fName, _ = QFileDialog.getSaveFileName(self, '保存文件', self.fileName,
                                                   'Markdown文件(*.md)')
            if fName != '':
                # self.editorTabWidget.openFileByInf(fName, 'UTF-8', "")
                self.filePath = fName
                self.fileName = os.path.split(fName)[1]
            else:
                return False

        with open(self.filePath, 'w+', encoding=self.fileEncoding) as f:
            f.write(self.fileContent)
        return True

    def saveFileAs(self) -> bool:
        fName, _ = QFileDialog.getSaveFileName(self, '另存文件为', self.fileName,
                                               'Markdown文件(*.md)')
        if fName != '':
            # self.editorTabWidget.openFileByInf(fName, 'UTF-8', "")
            self.filePath = fName
            self.fileName = os.path.split(fName)[1]

            with open(self.filePath, 'w+', encoding=self.fileEncoding) as f:
                f.write(self.fileContent)

            return True

        else:
            return False

    def commandSelectAll(self):
        """
        命令：全选
        :return:
        """
        self.codemirrorWidget.execCommand("selectAll")

    def commandUndo(self):
        """
        命令：撤销
        :return:
        """
        self.codemirrorWidget.execCommand("undo")

    def commandRedo(self):
        """
        命令：重做
        :return:
        """
        self.codemirrorWidget.execCommand("redo")

    def commandUndoSelection(self):
        """
        命令：撤销选择
        :return:
        """
        self.codemirrorWidget.execCommand("undoSelection")

    def commandRedoSelection(self):
        """
        命令：重做选择
        :return:
        """
        self.codemirrorWidget.execCommand("redoSelection")

    def commandFind(self):
        """
        命令：查找
        :return:
        """
        self.codemirrorWidget.execCommand("find")

    def commandReplace(self):
        """
        命令：替换
        :return:
        """
        self.codemirrorWidget.execCommand("replace")

    def skipTitle(self, href):
        self.previewWidget.skipTitle(href)

    def clipSelections(self):
        if self.selections:
            selection = self.selections
            content = ''
            for i in selection:
                content = content + i
            pyperclip.copy(content)
            # 清空选择内容
            self.deleteSelections()

    def copySelections(self):
        if self.selections:
            content = ''
            for i in self.selections:
                content = content + i
            pyperclip.copy(content)

    def deleteSelections(self):
        if self.selections:
            # 清空选择内容
            self.codemirrorWidget.clearSelectionContent()

    def paste(self):
        clipboardContent = pyperclip.paste()
        self.codemirrorWidget.insertContent(clipboardContent)

    def setVimMode(self, p: bool):
        self.codemirrorWidget.setVimMode(p)


