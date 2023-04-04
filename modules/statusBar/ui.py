from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QStatusBar, QPushButton, QCheckBox, QRadioButton


class StatusBarUI(QStatusBar):
    def __init__(self, parent=None):
        super(StatusBarUI, self).__init__(parent)

        self.setFixedHeight(23)

        self.setStyleSheet("QStatusBar::item{border: 0px}")

        self.setStyleSheet("border:0px;")

        self.button_widget_size = QSize(self.height() - 6, self.height() - 6)

        # 左边按钮
        self.tagsButton = QCheckBox(self)
        self.tagsButton.setObjectName("tagsButton")
        self.tagsButton.setProperty("class", "iconfontW")
        self.tagsButton.setCheckable(True)
        self.tagsButton.setText(chr(0xe6f5))
        self.tagsButton.setToolTip("组织结构")
        self.tagsButton.setStyleSheet("font-size:15px")
        self.addWidget(self.tagsButton)

        # 右侧按钮

        self.vimModeButton = QCheckBox(self)
        self.vimModeButton.setObjectName("vimModeButton")
        self.vimModeButton.setText('vim')
        self.vimModeButton.setToolTip("vim编辑模式")
        self.addPermanentWidget(self.vimModeButton)

        self.lineSeparatorButton = QPushButton(self)
        self.lineSeparatorButton.setFlat(True)
        self.lineSeparatorButton.setText('CRLF')
        self.lineSeparatorButton.setToolTip("行分割符")
        self.addPermanentWidget(self.lineSeparatorButton)

        self.encodingFormatButton = QPushButton(self)
        self.encodingFormatButton.setFlat(True)
        self.encodingFormatButton.setText('UTF-8')
        self.encodingFormatButton.setToolTip("文件编码")
        self.addPermanentWidget(self.encodingFormatButton)

        self.indentButton = QPushButton(self)
        self.indentButton.setFlat(True)
        self.indentButton.setText('4个空格')
        self.indentButton.setToolTip("缩进")
        self.addPermanentWidget(self.indentButton)

        self.editorModeButton = QPushButton(self)
        self.editorModeButton.setFlat(True)
        self.editorModeButton.setText('Markdown')
        self.editorModeButton.setToolTip("语法模式")
        self.addPermanentWidget(self.editorModeButton)

        self.readOnlyButton = QPushButton(self)
        self.readOnlyButton.setProperty("class", "iconfontW")
        self.readOnlyButton.setFlat(True)
        self.readOnlyButton.setToolTip("读写模式")
        # self.readOnlyButton.setFixedSize(self.button_widget_size)
        self.readOnlyButton.setText(chr(0xe678))
        self.readOnlyButton.setStyleSheet("font-size:13px;")
        # self.readOnlyButton.setIcon(QPixmap(":/icons/images/icons/cil-lock-unlocked.png"))  # cil-lock-locked
        # self.readOnlyButton.setIconSize(self.button_widget_size)
        self.addPermanentWidget(self.readOnlyButton)
