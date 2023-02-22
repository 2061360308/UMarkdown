from PySide6.QtWidgets import QSplitter

from .codemirrorWidget import CodemirrorWidget
from .previewWidget import PreviewWidget


class MarkdownWidgetUI(QSplitter):

    def __init__(self, parent=None):
        super(MarkdownWidgetUI, self).__init__(parent)

        self.setHandleWidth(2)

        self.codemirrorWidget = CodemirrorWidget(self)
        self.previewWidget = PreviewWidget(self)

        self.addWidget(self.codemirrorWidget)
        self.addWidget(self.previewWidget)

        self.setSizes([200, 200])