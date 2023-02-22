import os

from AppUMarkdown import appQSettings
from res import resources  # type: ignore
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QPalette, QBrush, QPixmap, QPainter, QIcon
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow, QDockWidget, QSplitter, QStackedWidget, QLabel

# from modules import StatusBar, ToolBar
from AppUMarkdown.application.modeIndex import moudelIndex
from modules.bgLabel import BgLabel
from modules.custom_grips import CustomGrip
from modules.editorTabWidget import EditorTabWidget
from modules.statusBar import StatusBar
from modules.title_menu_bar import TitleMenuBar
from modules.tocWidget import TocWidget
from modules.toolBar import ToolBar


class MainWindowUI(QMainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()

        self.tocWidget = None
        self.editorTabWidget = None
        self.moudelIndex = moudelIndex
        self.titleMenuBar = None
        self.stackedW = None
        self.splitter = None
        self.dockPanel = None
        self.toolBarW = None
        self.statusBarW = None
        self.setUpUI()

    def setUpUI(self):
        self.resize(800, 600)
        self.setWindowIcon(QIcon(":/icons/UMarkdownIcon_png"))

        self.bgImageLabel = BgLabel(self)
        self.bgImageLabel.setObjectName("bgImageLabel")
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.moudelIndex.bgImageLabel = self.bgImageLabel
        """ 检查并更新背景图片 """
        customBgPic = appQSettings.value('UiTheme/themeName')
        if customBgPic != "false":
            # 检查背景图片是否更换
            oldPic = moudelIndex.bgImageLabel.bgPath
            nowPic = appQSettings.value("customBgPic/path")

            if oldPic != nowPic:
                moudelIndex.bgImageLabel.setBg(nowPic)

        # 主窗体
        # self.editor = QWebEngineView()
        # self.editor.setAttribute(Qt.WA_TranslucentBackground)
        # self.editor.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, True)
        # self.editor.page().setBackgroundColor(QColor(0, 0, 0, 0))
        # # self.setCentralWidget(editor)
        # self.editor.setUrl(QUrl("file:///%s" % "codemirror/MarkdownEditor.html"))

        self.editorTabWidget = EditorTabWidget(self)
        self.editorTabWidget.setObjectName("editorTabWidget")
        self.moudelIndex.editorTabWidget = self.editorTabWidget

        # 状态栏
        self.statusBarW = StatusBar(self)
        self.statusBarW.setObjectName("statusBarW")
        self.setStatusBar(self.statusBarW)
        self.moudelIndex.statusBarW = self.statusBarW

        # 工具栏
        self.toolBarW = ToolBar(self)
        self.toolBarW.setObjectName("toolBarW")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBarW)
        self.moudelIndex.toolBarW = self.toolBarW

        self.splitter = QSplitter(self)
        self.splitter.setObjectName("MainWindowSplitter")
        self.splitter.setChildrenCollapsible(False)  # 不允许折叠
        self.splitter.setHandleWidth(2)
        self.moudelIndex.splitter = self.splitter

        # 左侧工具栏（堆叠窗口）
        self.stackedW = QStackedWidget(self)
        self.stackedW.setMinimumWidth(20)
        self.stackedW.setObjectName("stackedW")
        self.stackedW.hide()
        self.moudelIndex.stackedW = self.stackedW

        # toc
        self.tocWidget = TocWidget(self)
        self.moudelIndex.tocWidget = self.tocWidget
        self.stackedW.addWidget(self.tocWidget)

        self.splitter.addWidget(self.stackedW)
        self.splitter.addWidget(self.editorTabWidget)

        self.setCentralWidget(self.splitter)
        # self.splitter.setContentsMargins(5,0,5,0)
        # self.splitter.set
        # self.splitter.setStyleSheet("")
        
        # 自定义标题菜单栏
        self.titleMenuBar = TitleMenuBar(self)
        self.titleMenuBar.setObjectName("titleMenuBar")
        self.setMenuBar(self.titleMenuBar)

        # 替代边框， 采用PyDracula
        no_grip_color = True
        self.left_grip = CustomGrip(self, Qt.LeftEdge, no_grip_color)
        self.right_grip = CustomGrip(self, Qt.RightEdge, no_grip_color)
        self.top_grip = CustomGrip(self, Qt.TopEdge, no_grip_color)
        self.bottom_grip = CustomGrip(self, Qt.BottomEdge, no_grip_color)

    def resize_grips(self):
        if hasattr(self, "left_grip"):
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    def resizeEvent(self, event):
        if hasattr(self, "left_grip"):
            self.left_grip.release_right()
