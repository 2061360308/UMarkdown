import os.path
import sys

import pypandoc
from PySide6.QtWidgets import QFileDialog

import pyperclip
from jinja2 import FileSystemLoader, Environment

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

    readOnly = False  # 只读模式

    changeMark = None  # 改动标识

    lastState = None  # 上次分配状态

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
        if self.filePath is not None:
            self.previewWidget.setFilePath(os.path.split(self.filePath)[0])
        else:
            self.previewWidget.setFilePath("")

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

    def updateLastState(self):
        """
        更新最新的分配状态
        :return:
        """
        self.lastState = self.saveState()

    def restoreLastState(self):
        """
        恢复上次的状态
        :return:
        """
        if self.lastState:
            self.restoreState(self.lastState)
        else:
            self.setSizes([1, 1])

    def tocUpdate(self, tocHtml=None):
        # 更新文章的toc属性
        if tocHtml is not None:
            self.fileToc = tocHtml

        # 如果statusBarW的TocWidget处于打开状态那么更新他的内容
        if hasattr(moudelIndex, 'statusBarW'):
            tocOpen = moudelIndex.statusBarW.tagsButton.isChecked()
            if tocOpen:
                moudelIndex.tocWidget.updateToc(self.fileToc)

    def getToc(self):
        return self.fileToc

    def updateReadOnly(self):
        self.readOnly = not self.readOnly
        self.codemirrorWidget.setReadOnly(self.readOnly)
        return self.readOnly

    def getPreviewHtml(self):
        return self.previewWidget.previewHtml

    def updateTheme(self):
        """
        重新加载css文件
        :return:
        """
        # 这里只要codemirrorWidget更新就好，预览界面只是用了滚动条样式不需要更新
        self.codemirrorWidget.updateTheme()

    def updatePreviewTheme(self, old, new):
        """
        更新预览主题
        :param old:
        :param new:
        :return:
        """
        self.previewWidget.updatePreviewTheme(old, new)

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
        fName, a = QFileDialog.getSaveFileName(self, '另存文件为', self.fileName,
                                               'Markdown文件(*.md);;Word文档(*.docx);;电子书文档(*.epub);;网页(*.html *.htm);;图片('
                                               '*.jpg *.jpeg);;图片(*.png)')

        if fName != '':
            # self.editorTabWidget.openFileByInf(fName, 'UTF-8', "")
            filePath = fName
            fileName = os.path.split(fName)[1]
            suffix = os.path.splitext(fName)[1]

            if suffix == ".md":
                with open(filePath, 'w+', encoding=self.fileEncoding) as f:
                    f.write(self.fileContent)
            elif suffix == ".html":
                print(self.previewWidget.previewHtml)
                # 生成html
                path_dir = r"res/template"  # 模板文件所在的绝对路径
                loader = FileSystemLoader(searchpath=path_dir)
                env = Environment(loader=loader, variable_start_string="{{", variable_end_string="}}",
                                  block_start_string='{%',
                                  block_end_string='%}')

                template = env.get_template("outfile_html.template")  # 模板文件
                htmlContent = template.render({'previewHtml': self.previewWidget.previewHtml})

                # 创建html输出目录
                htmlDir = os.path.join(os.path.split(fName)[0], fileName.replace(suffix, ""))
                os.mkdir(htmlDir)

                # 输出html
                with open(os.path.join(htmlDir, fileName), "w+", encoding=self.fileEncoding) as f:
                    f.write(htmlContent)

                # 获取对应css文档，复制

            elif suffix == ".docx" or suffix == ".epub":
                self.pandocConvent(suffix, filePath)
            else:
                pass

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

    def changeSelectionContent(self, n_text: str):
        """
        更改选中的内容
        :param n_text: 新的内容
        :return:
        """
        self.codemirrorWidget.changeSelectionContent(n_text)

    def insertContent(self, content):
        """
        当前光标位置插入内容
        :param content: 新的内容
        :return:
        """
        self.codemirrorWidget.insertContent(content)

    def paste(self):
        clipboardContent = pyperclip.paste()
        self.codemirrorWidget.insertContent(clipboardContent)

    def setVimMode(self, p: bool):
        self.codemirrorWidget.setVimMode(p)

    def pandocConvent(self, conventType: str, filePath: str):
        '''
        调用pandoc
        :param conventType: 转换的格式
        :param filePath: 输出文件完整路径
        '''
        """
            转化文件的格式。
            convert(source, to, format=None, extra_args=(), encoding=‘utf-8‘, outputfile=None, filters=None)
            parameter-
                source：源文件
                to：目标文件的格式，比如html、rst、md等
                format：源文件的格式，比如html、rst、md等。默认为None，则会自动检测
                encoding：指定编码集
                outputfile：目标文件，比如test.html（注意outputfile的后缀要和to一致）
        """

        # 处理给出后缀存在加点的情况
        if conventType.startswith("."):
            conventType = conventType[1:]

        # 添加环境变量
        dirname = os.path.dirname(os.path.realpath(sys.argv[0]))
        os.environ["path"] = os.environ["path"] + os.path.join(dirname, "Pandoc") + ";"

        pypandoc.convert_text(self.fileContent,
                              conventType,
                              format="md",
                              encoding=self.fileEncoding,
                              outputfile=filePath
                              )
