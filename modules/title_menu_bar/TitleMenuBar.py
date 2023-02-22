"""
用QMenuBar改装的标题栏
"""
import os

from PySide6 import QtGui
from PySide6.QtGui import QMouseEvent, QIcon, QAction, QFont
from PySide6.QtWidgets import QMenuBar, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QMenu
from PySide6.QtCore import Qt, QSize


class TitleMenuBar(QMenuBar):
    _move_drag = False

    systemButtonSize = QSize(50, 30)

    def __init__(self, parent=None):
        super(TitleMenuBar, self).__init__(parent)

        self.pressPoint = None
        self.setAttribute(Qt.WA_StyledBackground)  # 允许qss样式
        self.setObjectName("TitleMenuBar")

        # self.parent().installEventFilter(self)  # 注册监视器监视父组件事件
        # self.parent().setWindowFlags(Qt.FramelessWindowHint)
        # self.parent().setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowSystemMenuHint)
        self.parent().setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # 添加按钮面板，最小，最大，关闭
        self.button_widget = QWidget(self)  # 按钮面板
        self.button_widget.setStyleSheet("background-color:rgba(0,0,0,0)")
        self.horizontalLayout = QHBoxLayout(self.button_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.minButton = QPushButton(self.button_widget)
        self.minButton.setFixedSize(self.systemButtonSize)
        # self.minButton.setText("－")
        # self.minButton.setIcon(QIcon(":/icons/images/icons/icon_minimize"))
        self.minButton.setText(chr(0xe697))
        self.minButton.setObjectName(u"minButton")
        self.minButton.setProperty('class', 'iconfontW')
        self.minButton.setFlat(True)
        self.minButton.clicked.connect(self.min_button_clicked)
        self.horizontalLayout.addWidget(self.minButton)

        self.maxButton = QPushButton(self.button_widget)
        self.maxButton.setFixedSize(self.systemButtonSize)
        self.maxButton.setText(chr(0xe65b))
        self.maxButton.setObjectName(u"maxButton")
        self.maxButton.setProperty('class', 'iconfontW')
        self.maxButton.setFlat(True)
        self.maxButton.clicked.connect(self.max_button_clicked)
        self.horizontalLayout.addWidget(self.maxButton)

        self.closeButton = QPushButton(self.button_widget)
        self.closeButton.setFixedSize(self.systemButtonSize)
        self.closeButton.setStyleSheet("QPushButton:hover{background-color:#de0712;}")
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setProperty('class', 'iconfontW')
        self.closeButton.clicked.connect(self.close_button_clicked)
        self.closeButton.setText(chr(0xe666))
        self.closeButton.setIconSize(QSize(20, 20))
        self.closeButton.setFlat(True)
        # self.closeButton.setText("x")
        self.horizontalLayout.addWidget(self.closeButton)

        self.button_widget.setLayout(self.horizontalLayout)
        self.setCornerWidget(self.button_widget, Qt.TopRightCorner)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self._move_drag = True
        self.pressPoint = event.globalPosition().toPoint()
        super(TitleMenuBar, self).mousePressEvent(event)  # 激活父事件，是动作可以被触发

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._move_drag:
            # self.parent().move(event.globalPos() - self.move_DragPosition)
            self.max_button_update()  # 拖动退出最大化状态
            self.parent().showNormal()
            delta = event.globalPosition().toPoint() - self.pressPoint
            self.parent().move(self.parent().pos() + delta)
            self.pressPoint = event.globalPosition().toPoint()
        super(TitleMenuBar, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._move_drag = False
        super(TitleMenuBar, self).mouseReleaseEvent(event)

    def menu_item_clicked(self):
        self._move_drag = False

    # 菜单子项被点击，取消移动标识

    def addMenu(self, menu) -> QMenu:
        menu = super(TitleMenuBar, self).addMenu(menu)
        menu.aboutToShow.connect(self.menu_item_clicked)
        menu.aboutToHide.connect(self.menu_item_clicked)
        return menu

    # 重写添加菜单事件，将他的展示和隐藏事件绑定到菜单子项点击事件，阻止点击它时产生的移动窗口事件

    def addAction(self, action: QAction) -> None:
        # QMenuBar.addAction()
        super(TitleMenuBar, self).addAction(action)
        action.hovered.connect(self.menu_item_clicked)
        action.triggered.connect(self.menu_item_clicked)
        # 应对类似 self.menubar.addAction(self.menu_file.menuAction()) 写法
        if action.menu() is not None:
            action.menu().aboutToShow.connect(self.menu_item_clicked)
            action.menu().aboutToHide.connect(self.menu_item_clicked)

    # 重写添加action，将他的鼠标悬浮和点击事件都绑定到菜单子项点击事件，阻止点击它时产生的移动窗口事件

    """
    接下来监听父类窗口的相关事件，因为我不想让父窗口代码太乱
    """

    # def eventFilter(self, widget, event):
    #     if widget == self.parent() and type(event) == QMouseEvent:
    #         pass
    #         # print(event)
    #     return super(TitleMenuBar, self).eventFilter(widget, event)
    # return super(MyMenuBar, self).eventFilter(widget, event)

    # def mouseMoveEvent(self.parent(), QMouseEvent):
    #     # 判断鼠标位置切换鼠标手势
    #     if QMouseEvent.pos() in self._corner_rect:  # QMouseEvent.pos()获取相对位置
    #         self.setCursor(Qt.SizeFDiagCursor)
    #     elif QMouseEvent.pos() in self._bottom_rect:
    #         self.setCursor(Qt.SizeVerCursor)
    #     elif QMouseEvent.pos() in self._right_rect:
    #         self.setCursor(Qt.SizeHorCursor)
    #
    #     # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
    #     # 没有定义左方和上方相关的5个方向，主要是因为实现起来不难，但是效果很差，拖放的时候窗口闪烁，再研究研究是否有更好的实现
    #     if Qt.LeftButton and self._right_drag:
    #         # 右侧调整窗口宽度
    #         self.resize(QMouseEvent.pos().x(), self.height())
    #         QMouseEvent.accept()
    #     elif Qt.LeftButton and self._bottom_drag:
    #         # 下侧调整窗口高度
    #         self.resize(self.width(), QMouseEvent.pos().y())
    #         QMouseEvent.accept()
    #     elif Qt.LeftButton and self._corner_drag:
    #         #  由于我窗口设置了圆角,这个调整大小相当于没有用了
    #         # 右下角同时调整高度和宽度
    #         self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
    #         QMouseEvent.accept()
    #     elif Qt.LeftButton and self._move_drag:
    #         # 标题栏拖放窗口位置
    #         self.move(QMouseEvent.globalPos() - self.move_DragPosition)
    #         QMouseEvent.accept()
    def max_button_update(self):
        if self.parent().windowState() == Qt.WindowMaximized:
            self.maxButton.setText(chr(0xe661))
        else:
            self.maxButton.setText(chr(0xe65b))

    def max_button_clicked(self):
        if self.parent().windowState() == Qt.WindowMaximized:
            self.parent().showNormal()
            self.max_button_update()
        elif self.parent().windowState() == Qt.WindowNoState:
            self.parent().showMaximized()
            self.max_button_update()

    def min_button_clicked(self):
        self.parent().showMinimized()

    def close_button_clicked(self):
        self.parent().close()
