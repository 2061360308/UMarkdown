from PySide6.QtWidgets import QToolBar

from modules.toolBar.ui import ToolBarUI


class ToolBar(ToolBarUI):
    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)

