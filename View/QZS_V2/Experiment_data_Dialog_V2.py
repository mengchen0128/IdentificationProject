import os
import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, \
    QFileDialog, QCheckBox, QMessageBox, QWidget, QLineEdit, QGridLayout, QRadioButton
from numpy import ndarray

BSER_DIR=os.path.dirname(os.path.realpath(__file__))

class Experiment_data_Dialog_V2(QWidget):


    input_data=pyqtSignal(ndarray)

    def __init__(self,*args,**kwargs):
        super(Experiment_data_Dialog_V2, self).__init__(*args,**kwargs)
        self.fileName = ""

        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):

        self.native = QCheckBox()
        self.native.setText("Use native file dialog.")
        self.native.setChecked(True)
        if sys.platform not in ("win32", "darwin"):
            self.native.hide()
        self.setLayout(self.init_file())

    def dragEnterEvent(self, evn):
        self.openFileNameLabel.setText(evn.mimeData().text())
        self.save_file_path(evn.mimeData().text())
        # 鼠标放开函数事件
        evn.accept()
    def dragMoveEvent(self, evn):
        self.openFileNameLabel.setStyleSheet('background: rgb(%d, %d, %d);' % (
                220, 220, 220))

    def init_file(self):

        mainLayout = QGridLayout()

        self.form_layout = QVBoxLayout()

        self.openFileNameEdit = QLineEdit()

        self.openFileNameButton = QPushButton("打开实验数据")

        self.label=QLabel()
        self.label.setPixmap(QPixmap(os.path.join(BSER_DIR, "images/drag_file.png")))
        self.label.setAlignment(Qt.AlignCenter)


        self.radio1 = QRadioButton("初始数据")
        self.radio2 = QRadioButton("谐波系数数据")
        self.radio1.setChecked(True)


        self.openFileNameButton.clicked.connect(self.setOpenFileName)

        mainLayout.addWidget(self.radio1, 1, 0,)
        mainLayout.addWidget(self.radio2, 1, 1)
        mainLayout.addWidget(self.openFileNameButton, 2, 0)
        mainLayout.addWidget(self.openFileNameEdit, 2, 1)


        import json

        filepath = os.path.join(BSER_DIR, "database/file_path.json")
        if os.path.exists(filepath):
            with open(filepath, mode='r', encoding='utf-8') as f:
                data = f.read()
                if data!="":
                    self.fileName = json.loads(data)
                    f.close()
                    self.openFileNameEdit.setText(self.fileName)
                else : pass

        self.form_layout.addWidget(self.label)
        self.form_layout.addLayout(mainLayout)
        return self.form_layout

    def setOpenFileName(self):
        """ 设置完成时的按钮"""
        options = QFileDialog.Options()
        if not self.native.isChecked():
            options |= QFileDialog.DontUseNativeDialog

        self.fileName, _ = QFileDialog.getOpenFileName(self,
                "QFileDialog.getOpenFileName()", "./",
                "All Files (*);;Mat Files (*.mat)", options=options)
        if self.fileName:

            self.openFileNameEdit.setText(self.fileName)
            self.save_file_path(self.fileName)

            # Data = scipy.io.loadmat(fileName)
            # PreData = Data['PreprocessedData']
            #
            # self.input_data.emit(PreData)
        else:
            QMessageBox.warning(self, "警告","没有选中任何文件")


    def save_file_path(self,filename):
        import os
        import json
        file_object = open(os.path.join(BSER_DIR, "database/file_path.json"), mode='w', encoding='utf-8')
        json.dump(filename, file_object)
        file_object.close()

