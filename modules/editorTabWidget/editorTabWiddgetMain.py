import json
import os.path

import chardet
from PySide6.QtWidgets import QWidget

from AppUMarkdown import appQSettings
from AppUMarkdown.application.modeIndex import moudelIndex
from .ui import EditorTabWidgetUI
from modules.markdownWidget import MarkdownWidget


class EditorTabWidget(EditorTabWidgetUI):
    def __init__(self, parent=None):
        super(EditorTabWidget, self).__init__(parent)

        self.tabCloseRequested.connect(self.tabCloseClicked)
        self.currentChanged.connect(self.currentTabChanged)
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

    def updatePreviewTheme(self, old, new):
        """
        更新预览主题
        :return:
        """
        # 先更新当前显示文档的，然后依次更新
        if self.currentWidget() is None:
            return
        self.currentWidget().updatePreviewTheme(old, new)
        currentIndex = self.currentIndex()
        for i in range(self.count()):
            if i != currentIndex:
                widget = self.widget(i)
                widget.updatePreviewTheme(old, new)

    def addTab(self, widget: QWidget, arg__2: str) -> int:
        super(EditorTabWidget, self).addTab(widget, arg__2)
        self.tabNumChange()

    def removeTab(self, index: int) -> None:
        super(EditorTabWidget, self).removeTab(index)
        self.tabNumChange()

    def currentTabChanged(self, index: int) -> None:
        """
        当前tab改变
        :param index:
        :return:
        """
        widget = self.widget(index)
        widget.tocUpdate()

        readOnly = widget.readOnly
        if hasattr(moudelIndex, "statusBarW"):
            moudelIndex.statusBarW.updateReadOnlyButton(readOnly)

    def updateReadOnly(self):
        """
        更新只读模式状态
        :return:
        """

        widget = self.currentWidget()
        readOnly = widget.updateReadOnly()

        moudelIndex.statusBarW.updateReadOnlyButton(readOnly)

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
            print(fileEncoding)
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

    def registerHistory(self, path):
        """
        注册历史记录,
        :param path: 文件的路径
        :return:
        """

        appQSettings.beginGroup("History")
        recentFiles = appQSettings.value("recentFiles")

        if recentFiles is None:
            appQSettings.setValue("recentFiles", json.dumps([path]))
        else:
            recentFiles = json.loads(recentFiles)

            if path in recentFiles:
                recentFiles.remove(path)

            recentFiles.insert(0, path)
            appQSettings.setValue("recentFiles", json.dumps(recentFiles))
        appQSettings.endGroup()

        moudelIndex.mainWindow.updateRecentFilesMenu(recentFiles)

        # 更新最近列表

    def tabCloseClicked(self, index):
        widget = self.widget(index)
        path = widget.filePath
        if widget.saveFile():
            self.removeTab(index)
            self.registerHistory(path)

    def closeAll(self):
        """
        关闭所有标签页
        :return:
        """
        for i in range(self.count()):
            widget = self.widget(i)
            if widget.saveFile():
                self.removeTab(i)

    def saveFile(self):
        widget = self.currentWidget()
        widget.saveFile()

    def saveFileAll(self):
        """
        保存所有文件
        :return:
        """
        for i in range(self.count()):
            widget = self.widget(i)
            widget.saveFile()

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

    def setVimMode(self, p: bool):
        """
        设置vim模式
        :param p: ture开启， false 关闭
        :return:
        """
        for i in range(self.count()):
            widget = self.widget(i)
            widget.setVimMode(p)

    def preview(self):
        """
        进入预览模式
        :return:
        """
        widget = self.currentWidget()
        widget.updateLastState()
        widget.setSizes([0, 1])
        # for i in range(self.count()):
        #     widget = self.widget(i)
        #     widget.setSizes([0, 1])

    def edited(self):
        """
        进入编辑模式
        :return:
        """
        widget = self.currentWidget()
        widget.restoreLastState()
        # for i in range(self.count()):
        #     widget = self.widget(i)
        #     widget.setSizes([1, 1])
