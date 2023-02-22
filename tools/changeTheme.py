import os
from xml.dom.minidom import parse
import xml.dom.minidom
from AppUMarkdown.application.extensions import load_stylesheet

from AppUMarkdown import appQSettings
from AppUMarkdown.application.modeIndex import moudelIndex
from tools.themeGenerator import uiQssGenerator, uiCssGenerator


def changeTheme():
    """
    更改主题
    :return:
    """
    # 判断是否启用了背景图片
    appQSettings.beginGroup('UiTheme')
    themeName = appQSettings.value('themeName')
    customFont = appQSettings.value('themeName')
    customBgPic = appQSettings.value('themeName')
    appQSettings.endGroup()

    """ 检查并更新背景图片 """
    if customBgPic != "false":
        # 检查背景图片是否更换
        oldPic = moudelIndex.bgImageLabel.bgPath
        nowPic = appQSettings.value("customBgPic/path")

        if oldPic != nowPic:
            moudelIndex.bgImageLabel.setBg(nowPic)

    # 获取当前主题文件内容
    themeFilePath = themeName + ".xml"
    themeFilePath = os.path.join(r"res/themes", themeFilePath)

    # 解析主题XML文档树
    DOMTree = xml.dom.minidom.parse(themeFilePath)
    collection = DOMTree.documentElement
    items = collection.getElementsByTagName("color")
    env_color = {}
    for item in items:
        name = "QTMATERIAL_" + item.getAttribute("name").upper()
        value = item.childNodes[0].data
        env_color[name] = value

    uiQssGenerator(env_color)
    uiCssGenerator(env_color, {})

    load_stylesheet()
    # 重新加载

    # 通知web浏览器更新主题
    moudelIndex.editorTabWidget.updateTheme()
#
# os.chdir("../")
# changeTheme()
