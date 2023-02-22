from PySide6.QtWidgets import QToolBar, QLabel


class ToolBarUI(QToolBar):
    def __init__(self, parent=None):
        super(ToolBarUI, self).__init__(parent)
        self.setObjectName("ToolBar")

        self.setFixedHeight(25)
        self.setMovable(False)

        blank_label = QLabel(self)  # 占位的label让按钮不至于顶到最左边
        blank_label.setFixedWidth(15)
        self.addWidget(blank_label)

        self.testLabel = QLabel(self)
        self.testLabel.setText("工具栏测试信息")
        self.addWidget(self.testLabel)