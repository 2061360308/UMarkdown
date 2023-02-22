from PySide6.QtCore import QObject


class MoudelIndex(QObject):
    """
    没有实际功能，充当模块的索引，MainWindow会从这里引入此对象，然后将示例化后的
    模块对象添加为其属性，其他模块同时引入此对象就可以方便地相互调用了
    """
    def __init__(self):
        super(MoudelIndex, self).__init__()


moudelIndex = MoudelIndex()
