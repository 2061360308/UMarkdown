# 保存，恢复窗口状态
from PySide6.QtWidgets import QMainWindow
from AppUMarkdown import appQSettings


def save_state(mainwindow: QMainWindow):
    appQSettings.beginGroup("MainWindowState")
    # appQSettings.setValue("State", mainwindow.saveState(-1))
    appQSettings.setValue("Geometry", mainwindow.saveGeometry())
    appQSettings.setValue("Maximized", mainwindow.isMaximized())
    appQSettings.setValue("SplitterState", mainwindow.splitter.saveState())
    appQSettings.setValue("SplitterHidden", mainwindow.stackedW.isHidden())
    appQSettings.setValue("vimMode", mainwindow.statusBarW.vimModeButton.isChecked())
    appQSettings.endGroup()


def load_state(mainwindow: QMainWindow):
    # 恢复窗体状态
    appQSettings.beginGroup("MainWindowState")
    # mainwindow.restoreState(appQSettings.value("State"))  # 恢复工具栏，QDockWidget状态，其实这里没有用
    mainwindow.restoreGeometry(appQSettings.value("Geometry"))  # 窗体Geometry
    if appQSettings.value("Maximized") == "true":  # 窗体最大化状态
        mainwindow.showMaximized()
        mainwindow.titleMenuBar.max_button_update()
    if appQSettings.value("SplitterHidden") == "false":
        mainwindow.stackedW.show()
        mainwindow.statusBarW.tagsButton.setChecked(True)
        mainwindow.statusBarW.tagsButton.setText(chr(0xe6f6))
    mainwindow.splitter.restoreState(appQSettings.value("SplitterState"))

    if appQSettings.value("vimMode") == "true":
        mainwindow.statusBarW.vimModeButton.setChecked(True)
    else:
        mainwindow.statusBarW.vimModeButton.setChecked(False)

    appQSettings.endGroup()
