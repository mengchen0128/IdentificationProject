import cgitb
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QDockWidget, QListWidget, QTextEdit, QVBoxLayout, QPushButton, \
    QTabWidget, QWidget, QApplication

cgitb.enable(format("text"))
from Controller.SignalDialogController import SignalDialogController


class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mainwindow2=None

    def initUI(self):
        self.create_menu()
        self.create_toolbar()
        self.setCentralWidget(self.create_dockcenter())
        self.addDockWidget(Qt.LeftDockWidgetArea, self.create_dockleft())
        self.addDockWidget(Qt.RightDockWidgetArea, self.create_dockright())
        self.addDockWidget(Qt.BottomDockWidgetArea, self.create_dockbottom())
        self.create_statusbar()
        self.resize(1200,800)
        self.setWindowTitle('参数辨识')

    def create_menu(self):
        bar = self.menuBar()  # 获取菜单栏

        file = bar.addMenu("文件")
        file.addAction("新建")

        save = QAction("保存",self)
        save.setShortcut("Ctrl + S")
        file.addAction(save)


        edit = bar.addMenu("编辑")
        edit.addAction("copy")
        edit.addAction("paste")

        quit = QAction("退出",self)
        file.addAction(quit)
        quit.triggered.connect(self.close)


    def create_toolbar(self):
        tb1 = self.addToolBar("File")

        new = QAction(QIcon('../images/new.png'), "new", self)
        tb1.addAction(new)

        open = QAction(QIcon('../images/open.png'), "open", self)
        tb1.addAction(open)

        save = QAction(QIcon('../images/save.png'), "save", self)
        tb1.addAction(save)

    def create_dockright(self):
        self.dockRight = QDockWidget("变量", self)

        self.listWidget = QListWidget()
        self.listWidget.insertItem(0,"item1")
        self.listWidget.insertItem(1,"item2")
        self.listWidget.insertItem(2,"item3")

        self.dockRight.setWidget(self.listWidget)
        self.dockRight.setFloating(False)

        return  self.dockRight
    def create_dockleft(self):
        self.dockLeft = QDockWidget("功能", self)
        self.listWidget2 = QListWidget()
        self.listWidget2.insertItem(0,"信号处理")
        self.listWidget2.insertItem(1,"非线性检测")
        self.listWidget2.insertItem(2,"模型")
        self.listWidget2.insertItem(3,"算法")

        self.listWidget2.currentRowChanged.connect(self.display)

        self.dockLeft.setWidget(self.listWidget2)
        self.dockLeft.setFloating(False)

        return self.dockLeft
    def create_dockbottom(self):
        self.dockBottom = QDockWidget("输出信息", self)

        self.textedit=QTextEdit()

        self.dockBottom.setWidget(self.textedit)
        self.dockBottom.setFloating(False)

        return self.dockBottom
    def create_dockcenter(self):
        layout = QVBoxLayout()
        layout.addWidget(QTextEdit())
        layout.addWidget(QPushButton('按钮2'))

        self.tabWidget=QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabWidget.addTab(self.tab1, "选项卡1")
        self.tabWidget.addTab(self.tab2, "选项卡2")
        self.tabWidget.addTab(self.tab3, "选项卡3")
        self.tabWidget.setTabsClosable(True)


        return self.tabWidget
    def create_statusbar(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')


    def display(self,index):
        #self.stack.setCurrentIndex(index)
        if index==0:
            if self.mainwindow2 is None:
                self.mainwindow2 = SignalDialogController()
            #self.mainwindow2.closed.connect(self.show)
            self.mainwindow2.show()
        elif index==1:
            pass
        elif index==2:
            pass
        else :
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainInterface()
    ex.show()
    sys.exit(app.exec_())
