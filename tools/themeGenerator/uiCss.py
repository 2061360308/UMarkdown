import os
from jinja2 import Environment, FileSystemLoader
from res import resources  # type: ignore
from AppUMarkdown import appQSettings


def uiCssGenerator(env_color, markdown_var):
    """
    生成web界面的css主题配置
    :param env_color: 环境变量中的基础颜色
    :param markdown_var: markdown的配置变量
    :return:
    """
    path_dir = r"res/template"  # 模板文件所在的绝对路径
    loader = FileSystemLoader(searchpath=path_dir)
    env = Environment(loader=loader)
    template = env.get_template("UI_theme.css.template")  # 模板文件

    transparency = float(appQSettings.value("customBgPic/opacity"))  # 透明度
    transparency_16 = hex(int(255 * transparency))[2:].upper()
    # 单一数字补齐
    if len(transparency_16) == 1:
        transparency_16 = transparency_16 + transparency_16

    markdown_var = {
        "theme_name": "dracula",
        "transparency_16": transparency_16,
        "cursor_color": "#000000",
        "default_color": "#f1fa8c",
        "var_keyword": "#e5900d",
        "var_string": "#50fa7b",
        "var_string_2": "#896724",
        "var_number": "#f1fa8c",
        "var_variable": "#896724",
        "var_variable_2": "#6272a4",
        "var_variable_3": "#896724",
        "var_def": "#d0cccc",
        "var_operator": "#ffb86c",
        "var_atom": "#896724",
        "var_meta": "#896724",
        "var_tag": "#896724",
        "var_attribute": "#896724",
        "var_qualifier": "#896724",
        "var_property": "#ff79c6",
        "var_builtin": "#896724",
        "var_type": "#896724",
    }

    env_var = {}
    env_var.update(env_color)
    env_var['transparency_16'] = transparency_16
    env_var.update(markdown_var)

    buf = template.render(env_var)
    with open(os.path.join("codemirror/editor/css", "theme.css"), "w", encoding='utf-8') as fp:
        fp.write(buf)
