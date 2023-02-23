import os.path

from PySide6.QtWidgets import QFileDialog

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

        self.codemirrorWidget.contentChangeSignal.connect(self.connectChange)
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

