from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from modules import MainWindow
from .app import app
from .extensions import load_stylesheet, appQSettings

mainWindow = MainWindow()

load_stylesheet()
appQSettings.setValue("Application/name", "UMainWindow")