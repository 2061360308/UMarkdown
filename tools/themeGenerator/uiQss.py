from jinja2 import FileSystemLoader, Environment
from AppUMarkdown.application.extensions import appQSettings


def uiQssGenerator(env_color):
    path_dir = r"res/template"  # 模板文件所在的绝对路径
    loader = FileSystemLoader(searchpath=path_dir)
    env = Environment(loader=loader, variable_start_string="<", variable_end_string=">", block_start_string='{%',
                      block_end_string='%}')
    template = env.get_template("UI_theme.qss.template")  # 模板文件

    transparency = float(appQSettings.value("customBgPic/opacity"))  # 透明度
    transparency_16 = hex(int(255 * transparency))[2:].upper()
    # 单一数字补齐
    if len(transparency_16) == 1:
        transparency_16 = transparency_16 + transparency_16

    # env_color = {
    #     'QTMATERIAL_PRIMARYCOLOR': '#1de9b6',
    #     'QTMATERIAL_PRIMARYLIGHTCOLOR': '#6effe8',
    #     'QTMATERIAL_SECONDARYCOLOR': '#232629',
    #     'QTMATERIAL_SECONDARYLIGHTCOLOR': '#4f5b62',
    #     'QTMATERIAL_SECONDARYDARKCOLOR': '#31363b',
    #     'QTMATERIAL_PRIMARYTEXTCOLOR': '#000000',
    #     'QTMATERIAL_SECONDARYTEXTCOLOR': '#ffffff',
    #     'transparency_16': transparency_16,
    # }

    env_var = {}
    env_var.update(env_color)
    env_var['transparency_16'] = transparency_16

    uiQss = template.render(env_var)
    with open("UI_theme.qss", "w", encoding='utf-8') as fp:
        fp.write(uiQss)
