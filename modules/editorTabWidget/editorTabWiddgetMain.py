import os.path

import chardet
from PySide6.QtWidgets import QWidget

from AppUMarkdown.application.modeIndex import moudelIndex
from .ui import EditorTabWidgetUI
from modules.markdownWidget import MarkdownWidget


class EditorTabWidget(EditorTabWidgetUI):
    def __init__(self, parent=None):
        super(EditorTabWidget, self).__init__(parent)

        self.tabCloseRequested.connect(self.tabCloseClicked)
        self.tabNumChange()

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

    def addTab(self, widget: QWidget, arg__2: str) -> int:
        super(EditorTabWidget, self).addTab(widget, arg__2)
        self.tabNumChange()

    def removeTab(self, index: int) -> None:
        super(EditorTabWidget, self).removeTab(index)
        self.tabNumChange()

    def openFile(self, filePath):
        """
        给定文件路径打开文件
        :param filePath:
        :return:
        """
        widget = MarkdownWidget(self)
        fileName = os.path.split(filePath)[1]
        self.addTab(widget, fileName)

        fileType = os.path.split(filePath)[1]
        with open(filePath, 'rb') as f:
            contentR = f.read()
            fileEncoding = chardet.detect(contentR)['encoding']  # 检测文件内容
        if fileEncoding is None:
            fileEncoding = "UTF-8"
        fileContent = contentR.decode(encoding=fileEncoding)
        widget.initFile(
            fileName=fileName,
            filePath=filePath,
            fileContent=fileContent,
            fileEncoding=fileEncoding,
            openEncoding=fileEncoding,
        )

        self.setCurrentWidget(widget)

    def openFileByInf(self, filePath, fileEncoding, fileContent):
        """
        给定文件信息打开文件
        :return:
        """
        widget = MarkdownWidget(self)
        fileName = os.path.split(filePath)[1]
        self.addTab(widget, fileName)
        widget.initFile(
            fileName=fileName,
            filePath=filePath,
            fileContent=fileContent,
            fileEncoding=fileEncoding,
            openEncoding=fileEncoding,
        )

        self.setCurrentWidget(widget)

    def openFabricateFile(self, fileName, fileEncoding, fileContent):
        """
        打开虚构的文件
        :param fileName:
        :param fileEncoding:
        :param fileContent:
        :return:
        """
        widget = MarkdownWidget(self)
        self.addTab(widget, fileName)
        widget.initFile(
            fileName=fileName,
            filePath=None,
            fileContent=fileContent,
            fileEncoding=fileEncoding,
            openEncoding=fileEncoding,
        )

        self.setCurrentWidget(widget)

    def tabCloseClicked(self, index):
        widget = self.widget(index)
        if widget.saveFile():
            self.removeTab(index)

    def closeAll(self):
        """
        关闭所有标签页
        :return:
        """
        for i in range(self.count()):
            widget = self.widget(i)
            if widget.saveFile():
                self.removeTab(i)

    def saveFileAs(self):
        """
        另存为
        :return:
        """
        widget = self.currentWidget()
        widget.saveFileAs()

    def tabNumChange(self):
        """
        tab 数发生改变
        :return:
        """
        num = self.count()

        if num == 0:
            self.noneOpenFiles()
            # 禁用动作
            # if hasattr(moudelIndex, "mainWindow"):
            #     for action in [moudelIndex.mainWindow.fileSaveAs,
            #                    moudelIndex.mainWindow.fileCloseAll,
            #                    moudelIndex.mainWindow.fileAttribute,
            #                    moudelIndex.mainWindow.fileSaveAll,
            #                    moudelIndex.mainWindow.fileReload,
            #                    moudelIndex.mainWindow.fileSaveAsTemplate]:
            #         action.setEnabled(False)

    def noneOpenFiles(self):
        """
        没有打开的文件时触发
        :return:
        """
        self.openFabricateFile("未命名.md", "UTF-8", "")
