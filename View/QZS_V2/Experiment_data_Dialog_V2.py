import os
import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, \
    QFileDialog, QCheckBox, QMessageBox, QWidget, QLineEdit, QGridLayout, QRadioButton
from numpy import ndarray

BSER_DIR=os.path.dirname(os.path.realpath(__file__))

class Experiment_data_Dialog_V2(QWidget):


    input_displacemeng_data=pyqtSignal(ndarray)
    input_coefficient_data=pyqtSignal(ndarray)

    def __init__(self,*args,**kwargs):
        super(Experiment_data_Dialog_V2, self).__init__(*args,**kwargs)
        self.fileName = ""


        self.init_ui()

    def init_ui(self):

        self.native = QCheckBox()
        self.native.setText("Use native file dialog.")
        self.native.setChecked(True)
        if sys.platform not in ("win32", "darwin"):
            self.native.hide()
        self.setLayout(self.init_file())



    def init_file(self):

        mainLayout = QGridLayout()

        self.form_layout = QVBoxLayout()

        self.openFileNameEdit = QLineEdit()

        self.openFileNameButton = QPushButton("打开实验数据")

        self.label=Label()
        self.label.setPixmap(QPixmap(os.path.join(BSER_DIR, "images/drag_file.png")))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.emit_filepath.connect(self.show_and_save)

        self.radio1 = QRadioButton("初始数据")
        self.radio2 = QRadioButton("谐波系数数据")
        self.radio1.setChecked(True)


        self.openFileNameButton.clicked.connect(self.setOpenFileName)


        mainLayout.addWidget(self.openFileNameButton, 0, 0)
        mainLayout.addWidget(self.openFileNameEdit, 0, 1)
        mainLayout.addWidget(self.radio1, 1, 0,)
        mainLayout.addWidget(self.radio2, 2, 0)


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

        fileName_dialog, _ = QFileDialog.getOpenFileName(self,
                "QFileDialog.getOpenFileName()", "./",
                "All Files (*);;Mat Files (*.mat)", options=options)
        if fileName_dialog:
            self.fileName=fileName_dialog
            self.openFileNameEdit.setText(fileName_dialog)
            self.save_file_path(fileName_dialog)

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

    def show_and_save(self,string):
        self.openFileNameEdit.setText(string)
        self.save_file_path(string)

class Label(QLabel):

    emit_filepath=pyqtSignal(str)
    def __init__(self,*args,**kwargs):

        super(Label, self).__init__(*args,**kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, evn):

        self.emit_filepath.emit(evn.mimeData().text())

        # 鼠标放开函数事件
        evn.accept()
    def dragMoveEvent(self, evn):
        self.setStyleSheet('background: rgb(%d, %d, %d);' % (
                220, 220, 220))