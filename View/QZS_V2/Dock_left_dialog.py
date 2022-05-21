from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem

Stylesheet = """
    /*去掉item虚线边框*/
    QListWidget, QListView, QTreeWidget, QTreeView {
        outline: 0px;
        border-radius: 10px;
    }
    /*设置左侧选项的最小最大宽度,文字颜色和背景颜色*/
    QListWidget {
        min-width: 150px;
        
        min-height:800px;
        
    }

    /*被选中时的背景颜色和左边框颜色*/
    QListWidget::item:selected {
        background: rgb(211, 211, 211);
        border-left: 2px solid rgb(9, 187, 7);
        padding: 30px;
    }
    QListWidget::item:hover {
        background: rgb(211, 211, 211);
        border-left: 2px solid rgb(9, 187, 7);
        padding: 30px;
    }
        QListWidget::item {

        border-left: 2px solid rgb(9, 187, 7);
        padding: 20px;
    }


    """




class dockleft(QWidget):

    def __init__(self, *args, **kwargs):
        super(dockleft, self).__init__(*args, **kwargs)
        self.initUi()
        self.setStyleSheet(Stylesheet)


    def initUi(self):
        form_list = [
            {"index":1,"title": "非线性度"},
            {"index":2,"title": "频响分析"},
            {"index":3,"title": "残差分析"},
            {"index":4,"title": "谐波幅值"},
        ]

        self.listWidget = QListWidget(self)

        self.listWidget.setFrameShape(QListWidget.NoFrame)



        for item in form_list:
            item = QListWidgetItem(
                QIcon('images/0%d.png' % item['index']), item['title'], self.listWidget)
            item.setSizeHint(QSize(60, 60))
            # 文字居中
            #item.setTextAlignment(Qt.AlignCenter)

