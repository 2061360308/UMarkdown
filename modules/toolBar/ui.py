from PySide6.QtWidgets import QToolBar, QLabel, QWidget, QSizePolicy, QHBoxLayout, QSpacerItem, QPushButton


class ToolBarUI(QToolBar):
    def __init__(self, parent=None):
        super(ToolBarUI, self).__init__(parent)
        self.setObjectName("ToolBar")

        self.setFixedHeight(25)
        self.setMovable(False)

        blank_label = QLabel(self)  # 占位的label让按钮不至于顶到最左边
        blank_label.setFixedWidth(15)
        self.addWidget(blank_label)

        # self.testLabel = QLabel(self)
        # self.testLabel.setText("工具栏测试信息")
        # self.addWidget(self.testLabel)

        self.previewButton = QPushButton(self)
        self.previewButton.setProperty("class", "iconfontW")
        self.previewButton.setText(chr(0xe64b))
        self.previewButton.setToolTip("预览")
        self.previewButton.setFlat(True)

        # 右侧布局盒子
        self.rightBox = QWidget(self)
        self.rightBox.setStyleSheet("background:rgba(0,0,0,0);")
        self.addWidget(self.rightBox)

        self.rightBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.rightBoxLayout = QHBoxLayout()
        self.rightBox.setLayout(self.rightBoxLayout)
        self.rightBoxLayout.setContentsMargins(0, 0, 15, 0)
        self.rightBoxLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.rightBoxLayout.addWidget(self.previewButton)
