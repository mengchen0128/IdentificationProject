from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QTabWidget, QWidget, QDockWidget, QTextEdit, QTableWidget, QPushButton, QHBoxLayout, QVBoxLayout


class ChildDialogUi1(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)

        menubar = MainWindow.menuBar()
        fileMenu = menubar.addMenu('File')




        self.tree = QTreeWidget()
      # 将组件添加到界面
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['key', 'value'])

        self.dockleft = QDockWidget("变量", self)
        self.dockleft.setWidget(self.tree)

        # 添加根目录
        root = QTreeWidgetItem(self.tree)
        # 设置key
        root.setText(0, '非线性检测方法')
        # 设置value
        root.setText(1, '方法')

        # 添加子目录的两种方式，第一种
        child1 = QTreeWidgetItem(root)
        child1.setText(0, '自由衰减响应信号')
        child1.setBackground(0, QColor(205, 201, 201))
        # 第二种
        child2 = QTreeWidgetItem()
        child2.setText(0, '正弦激励响应信号')
        root.addChild(child2)

        child3 = QTreeWidgetItem()
        child3.setText(0, '一般激励响应信号')
        root.addChild(child3)

        # 添加2层子节点
        child1_1 = QTreeWidgetItem(child1)
        child1_1.setText(0, '子节点1的子节点')

        self.tabWidget = QTabWidget()

        self.tabWidget.setTabsClosable(True)

        self.tab1 = QWidget()

        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)

        self.tab2 = QWidget()
        self.tab3 = QWidget()



        self.tabWidget.addTab(self.tab1, "自由衰减响应信号")
        self.tabWidget.addTab(self.tab2, "正弦激励响应信号")
        self.tabWidget.addTab(self.tab3, "一般激励响应信号")




        self.dockBottom = QDockWidget("输出信息", self)

        self.textedit=QTextEdit()

        self.dockBottom.setWidget(self.textedit)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(2)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectColumns)
        self.table.setSelectionMode(QTableWidget.SingleSelection)


        self.table.setColumnWidth(4, 200)
        self.table.setRowHeight(0, 40)


        self.dockRight = QDockWidget("变量", self)
        self.dockRight.setWidget(self.table)

        MainWindow.setCentralWidget(self.tabWidget)

        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockleft)

        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockRight)
        MainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.dockBottom)

    def tab11(self):
        self.importbutton=QPushButton()
        self.generatebutton = QPushButton()
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.importbutton)
        hbox.addWidget(self.generatebutton)

        self.tab1.setLayout(hbox)



