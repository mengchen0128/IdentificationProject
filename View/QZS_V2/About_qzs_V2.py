from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QDialog, QHBoxLayout, QListWidget, QStackedWidget, \
    QListWidgetItem

Stylesheet = """
    /*去掉item虚线边框*/
    QListWidget, QListView, QTreeWidget, QTreeView {
        outline: 0px;
    }
    /*设置左侧选项的最小最大宽度,文字颜色和背景颜色*/
    QListWidget {
        min-width: 120px;
        max-width: 120px;
    }
    /*被选中时的背景颜色和左边框颜色*/
    QListWidget::item:selected {
        background: rgb(52, 52, 52);
        border-left: 2px solid rgb(9, 187, 7);
    }
    /*鼠标悬停颜色*/
    HistoryPanel::item:hover {
        background: rgb(52, 52, 52);
    }

    """
class AboutDialog_V2(QDialog):

    def __init__(self, *args, **kwargs):
        super(AboutDialog_V2, self).__init__(*args, **kwargs)
        self.initUi()
        self.resize(800, 600)
        self.setStyleSheet(Stylesheet)
        self.setWindowTitle("帮助文件")


    def initUi(self):

        form_list = [
            {"title": "输入输出"},
            {"title": "FunTol"},
            {"title": "R"},
            {"title": "NT"},
            {"title": "ST"},
            {"title": "C"},
        ]


        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.listWidget = QListWidget(self)
        layout.addWidget(self.listWidget)
        self.stackedWidget = QStackedWidget(self)
        layout.addWidget(self.stackedWidget)

        self.listWidget.currentRowChanged.connect(
            self.stackedWidget.setCurrentIndex)

        self.listWidget.setFrameShape(QListWidget.NoFrame)


        for item in form_list:
            item = QListWidgetItem(
                QIcon(), item['title'], self.listWidget)
            item.setSizeHint(QSize(60, 60))
            # 文字居中
            item.setTextAlignment(Qt.AlignCenter)
        for i in range(20):
            label = QLabel('我是页面 %d' % i, self)
            label.setAlignment(Qt.AlignCenter)
            # 设置label的背景颜色(这里随机)
            # 这里加了一个margin边距(方便区分QStackedWidget和QLabel的颜色)
            self.stackedWidget.addWidget(label)