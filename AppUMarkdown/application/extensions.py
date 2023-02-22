# 存放扩展
import os.path
from res import resources  # type: ignore
from PySide6.QtCore import QSettings
from PySide6.QtGui import QFontDatabase
from qt_material import apply_stylesheet
from .app import app

# webView调试
DEBUG_PORT = '8989'
DEBUG_URL = 'http://127.0.0.1:%s' % DEBUG_PORT
os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = DEBUG_PORT

# 初始化QSettings
app.setOrganizationName("LuTong")
app.setOrganizationDomain("umarkdown.com")
app.setApplicationName("UMarkdown")
appQSettings = QSettings("AppUMarkdown/config/QSettings.ini", QSettings.IniFormat)

# 载入默认设置
if not os.path.isfile("AppUMarkdown/config/QSettings.ini"):
    # 主题名称
    appQSettings.beginGroup("UiTheme")
    appQSettings.setValue("themeName", "dark_teal")
    appQSettings.setValue("customFont", False)
    appQSettings.setValue("customBgPic", True)
    appQSettings.endGroup()

    appQSettings.beginGroup("customBgPic")
    appQSettings.setValue("path", "defaultBgPic.jpg")
    appQSettings.setValue("opacity", "0.7")
    appQSettings.endGroup()


# 加载字体
fontDb = QFontDatabase()
fontID = fontDb.addApplicationFont(":/fonts/iconfont")  # 此处的路径为qrc文件中的字体路径
fontFamilies = fontDb.applicationFontFamilies(fontID)
# print(fontFamilies)  # ['LXGW WenKai']

# 加载样式
def load_stylesheet():
    """
    加载style
    :return:
    """
    extra = {
        'density_scale': '-2',
        'QMenu': {
            'height': 8,
            'padding': '0px 0px 0px 0px',  # top, right, bottom, left
        }
    }

    theme = appQSettings.value("UiTheme/themeName") + ".xml"
    theme = os.path.join(r"res/themes", theme)

    apply_stylesheet(app, theme=theme, css_file='UI_theme.qss', extra=extra)
