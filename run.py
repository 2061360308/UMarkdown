import cgitb
import os
import sys

""" 下面这句很重要虽然它没有用到，但是去掉后调用QWebEngineView闪退 """
from PySide6.QtWebEngineWidgets import QWebEngineView

from AppUMarkdown.application.setup import app, mainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


cgitb.enable(format='text')
sys.excepthook = except_hook
mainWindow.show()
sys.exit(app.exec())
