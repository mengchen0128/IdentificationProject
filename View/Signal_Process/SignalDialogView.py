import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QWidget, QSplitter, QStackedWidget, \
    QFormLayout, QLineEdit, QPushButton, QAction, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class ChildDialogUi(object):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")

        MainWindow.resize(1200, 800)

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        MainWindow.setCentralWidget(self.centralwidget)

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.list = QListWidget()
        self.list.insertItem(0, '信号的生成')
        self.list.insertItem(1, '离散信号的分解')
        self.list.insertItem(2, '离散信号变换')

        self.splitter1 = QSplitter(Qt.Horizontal)

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        self.stack = QStackedWidget()

        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)

        self.splitter1.addWidget(self.list)
        self.splitter1.addWidget(self.stack)

        self.layout.addWidget(self.splitter1)

        self.list.currentRowChanged.connect(self.display)

        self.createActions()
        self.createMenus()

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        message = "Signal Process"
        self.statusbar.showMessage(message)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def newFile(self):
        pass

    def open(self):
        pass

    def save(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass

    def about(self):
        pass

    def aboutQt(self):
        pass

    def createActions(self):
        self.newAct = QAction("&New", self, shortcut=QKeySequence.New,
                              statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QAction("&Open...", self, shortcut=QKeySequence.Open,
                               statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QAction("&Save", self, shortcut=QKeySequence.Save,
                               statusTip="Save the document to disk", triggered=self.save)

        self.undoAct = QAction("&Undo", self, shortcut=QKeySequence.Undo,
                               statusTip="Undo the last operation", triggered=self.undo)

        self.redoAct = QAction("&Redo", self, shortcut=QKeySequence.Redo,
                               statusTip="Redo the last operation", triggered=self.redo)


        self.aboutAct = QAction("&About", self,
                                statusTip="Show the application's About box",
                                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                                  statusTip="Show the Qt library's About box",
                                  triggered=self.aboutQt)
        self.aboutQtAct.triggered.connect(QApplication.instance().aboutQt)

    def createMenus(self):

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)



        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def tab1UI(self):

        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.button = QPushButton('Matplot')

        layout = QFormLayout()

        self.lineEdit1 = QLineEdit()

        self.lineEdit2 = QLineEdit()

        self.lineEdit3 = QLineEdit()

        layout.addRow('频率', self.lineEdit1)
        layout.addRow('采样率', self.lineEdit2)
        layout.addRow('时长', self.lineEdit3)

        layout.addRow(self.toolbar)
        layout.addRow(self.canvas)
        layout.addRow(self.button)

        self.stack1.setLayout(layout)

    def tab2UI(self):
        layout = QFormLayout()
        layout.addRow('分解', QLineEdit())

        self.stack2.setLayout(layout)

    def tab3UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel('变换'))

        self.stack3.setLayout(layout)

    def display(self, index):
        self.stack.setCurrentIndex(index)