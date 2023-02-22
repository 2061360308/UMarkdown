import os.path

import chardet
from PySide6.QtWidgets import QWidget

from .ui import EditorTabWidgetUI
from modules.markdownWidget import MarkdownWidget


class EditorTabWidget(EditorTabWidgetUI):
    def __init__(self, parent=None):
        super(EditorTabWidget, self).__init__(parent)

        self.tabCloseRequested.connect(self.tabCloseClicked)

    def updateTheme(self):
        """
        更新主题
        :return:
        """
        # 先更新当前显示文档的，然后依次更新
        if self.currentWidget() is None:
            return
        self.currentWidget().updateTheme()
        currentIndex = self.currentIndex()
        for i in range(self.count()):
            if i != currentIndex:
                widget = self.widget(i)
                widget.updateTheme()

    def openFile(self, path):
        widget = MarkdownWidget(self)
        fileName = os.path.split(path)[1]
        self.addTab(widget, fileName)

        fileType = os.path.split(path)[1]
        with open(path, 'rb')as f:
            contentR = f.read()
            fileEncoding = chardet.detect(contentR)['encoding']  # 检测文件内容
        if fileEncoding is None:
            fileEncoding = "UTF-8"
        content = contentR.decode(encoding=fileEncoding)
        widget.initFile(
            fileName=fileName,
            filePath=path,
            fileType=fileType,
            fileContent=content,
            fileEncoding=fileEncoding,
            openEncoding=fileEncoding,
        )

        self.setCurrentWidget(widget)

    def tabCloseClicked(self, index):
        widget = self.widget(index)
        filePath = widget.filePath
        fileEncoding = widget.fileEncoding
        fileContent = widget.fileContent
        with open(filePath, 'w+', encoding=fileEncoding)as f:
            f.write(fileContent)
        self.removeTab(index)

