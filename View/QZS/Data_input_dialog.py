import cgitb
import os
import sys

import numpy as np
import scipy.io
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QPushButton, \
    QFileDialog, QFrame, QCheckBox, QDialogButtonBox, QGroupBox, QMessageBox, QListView
from numpy import ndarray

cgitb.enable(format("text"))

BSER_DIR=os.path.dirname(os.path.realpath(__file__))

class InputDialog(QDialog):

    signal_finish=pyqtSignal(str)
    input_data=pyqtSignal(ndarray)

    def __init__(self,*args,**kwargs):
        super(InputDialog, self).__init__(*args,**kwargs)
        self.frameStyle = QFrame.Sunken | QFrame.Panel
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("参数设置")
        self.resize(600, 600)

        self.native = QCheckBox()
        self.native.setText("Use native file dialog.")
        self.native.setChecked(True)
        if sys.platform not in ("win32", "darwin"):
            self.native.hide()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        layout.addLayout(self.init_header())

        layout.addLayout(self.init_table())

        layout.addLayout(self.init_file())

        layout.addLayout(self.init_footer())

        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def init_header(self):
        header_layout = QHBoxLayout()
        self.label  = QLabel("请在下方表格输入待辨识参数：")
        font = self.label.font()
        font.setPointSize(15)
        self.label.setFont(font)
        header_layout.addWidget(self.label)
        return header_layout

    def init_file(self):
        form_layout = QVBoxLayout()

        self.openFileNameLabel = QLabel()
        self.openFileNameLabel.setFrameStyle(self.frameStyle)
        self.openFileNameButton = QPushButton("打开实验数据")


        form_layout.addWidget(self.openFileNameButton)
        form_layout.addWidget(self.openFileNameLabel)


        self.openFileNameButton.clicked.connect(self.setOpenFileName)

        return form_layout

    def setOpenFileName(self):
        """ 设置完成时的按钮"""
        options = QFileDialog.Options()
        if not self.native.isChecked():
            options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                "QFileDialog.getOpenFileName()", self.openFileNameLabel.text(),
                "All Files (*);;Mat Files (*.mat)", options=options)
        if fileName:
            self.openFileNameLabel.setText(fileName)
            Data = scipy.io.loadmat(fileName)
            PreData = Data['PreprocessedData']

            self.input_data.emit(PreData)
        else:
            QMessageBox.warning(self, "警告","没有选中任何文件")

    def init_footer(self):
        footer_layout = QHBoxLayout()

    def init_table(self):
        table_layout = QHBoxLayout()

        self.table = QTableWidget(0, 2)

        self.table.setMinimumWidth(220)
        table_header=[
            {"field":"参数名","text":"参数名"},
            {"field": "初始估计值", "text": "初始估计值"},
            #{"field": "理论值", "text": "理论值"},
        ]
        for idx,info in enumerate(table_header):
            item=QTableWidgetItem()
            item.setText(info["text"])
            self.table.setHorizontalHeaderItem(idx,item)

        import json

        filepath = os.path.join(BSER_DIR, "database/parameters.json")
        with open(filepath, mode='r', encoding='utf-8') as f:
            data = f.read()
            datalist = json.loads(data)

        current_row_count = self.table.rowCount()

        for row_list in datalist:
            self.table.insertRow(current_row_count)
            for i, ele in enumerate(row_list):
                cell = QTableWidgetItem(str(ele))
                self.table.setItem(current_row_count, i, cell)
            current_row_count += 1

        groupBox = QGroupBox("Table editor")
        groupBoxLayout = QVBoxLayout()

        button_add = QPushButton("添加一行")
        button_delete = QPushButton("删除选中行")
        button_clear = QPushButton("清除所有参数")
        button_save = QPushButton("添加到右侧保存")
        save_other = QCheckBox("隐藏保存过的参数")


        button_add.clicked.connect(self.add_table_row)
        button_delete.clicked.connect(self.delete_table_row)
        button_clear.clicked.connect(self.remove_table_row)
        save_other.toggled.connect(self.hideChild)

        groupBoxLayout.addWidget(button_add)
        groupBoxLayout.addWidget(button_delete)
        groupBoxLayout.addWidget(button_clear)
        groupBoxLayout.addWidget(button_save)
        groupBoxLayout.addWidget(save_other)





        groupBoxLayout.addStretch()

        groupBox.setLayout(groupBoxLayout)

        self.anoter_list = QListView()

        table_layout.addWidget(self.table)
        table_layout.addWidget(groupBox)
        table_layout.addWidget(self.anoter_list)
        table_layout.addStretch()
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)

        return table_layout
    def hideChild(self,v):
        self.anoter_list.setVisible(not v)




    def accept(self):

        data_dict=[ [
                "" for _ in range(self.table.columnCount())
            ] for _ in range(self.table.rowCount())    ]

        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                it = self.table.item(row, col)
                if it and it.text():
                    data_dict[row][col]=self.table.item(row,col).text().strip()
                else :
                    QMessageBox.warning(self, "警告", "参数值不能为空或有空行！")
                    return
        import os
        import json
        file_object = open(os.path.join(BSER_DIR, "database/parameters.json"), mode='w', encoding='utf-8')
        json.dump(data_dict, file_object)
        file_object.close()


        finish_str="---数据输入及参数设置---"
        self.signal_finish.emit(finish_str)
        self.close()

        #保存参数
    def add_table_row(self):
        current_row_count = self.table.rowCount()
        self.table.insertRow(current_row_count)
    def delete_table_row(self):
        row_list = self.table.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "没有选中任何行")
            return
        row_list.reverse()
        for row_object in row_list:
            index = row_object.row()
            self.table.removeRow(index)
    def remove_table_row(self):

        reply = QMessageBox.question(self, "QMessageBox.question()",
                                     "确定要删除所有参数吗？",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            for i in range(0,self.table.rowCount())[::-1]:
                self.table.removeRow(i)

        elif reply == QMessageBox.No:
            pass
        else:
            pass
