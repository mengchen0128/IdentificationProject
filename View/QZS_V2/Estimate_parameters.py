import os

import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, \
    QMessageBox, QHeaderView, QFormLayout, QLabel, QLineEdit, QDialogButtonBox
from numpy import ndarray

BSER_DIR=os.path.dirname(os.path.realpath(__file__))

class Estimate_parameters(QDialog):

    signal_finish=pyqtSignal(str)
    input_data=pyqtSignal(ndarray)

    def __init__(self,*args,**kwargs):
        super(Estimate_parameters, self).__init__(*args,**kwargs)
        self.init_ui()

    def init_ui(self):



        layout = QVBoxLayout()


        layout.addLayout(self.init_table())

        self.setLayout(layout)



    def init_table(self):
        table_layout = QHBoxLayout()

        self.table = QTableWidget(0, 2)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table_header=[
            {"field":"参数名","text":"参数名"},
            {"field": "初始估计值", "text": "初始估计值"},
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
            f.close()
        current_row_count = self.table.rowCount()

        for row_list in datalist:
            self.table.insertRow(current_row_count)
            for i, ele in enumerate(row_list):
                cell = QTableWidgetItem(str(ele))
                self.table.setItem(current_row_count, i, cell)
            current_row_count += 1


        groupBoxLayout = QVBoxLayout()

        button_add = QPushButton("添加一个参数")
        button_delete = QPushButton("删除选中参数")
        button_clear = QPushButton("清除所有参数")
        button_matrix = QPushButton("输入质量矩阵")






        button_add.clicked.connect(self.add_table_row)
        button_delete.clicked.connect(self.delete_table_row)
        button_clear.clicked.connect(self.remove_table_row)
        button_matrix.clicked.connect(self.receive_matrix)


        groupBoxLayout.addWidget(button_add)
        groupBoxLayout.addWidget(button_delete)
        groupBoxLayout.addWidget(button_clear)
        groupBoxLayout.addWidget(button_matrix)



        groupBoxLayout.addStretch()


        table_layout.addWidget(self.table)
        table_layout.addLayout(groupBoxLayout)


        self.table.setContextMenuPolicy(Qt.CustomContextMenu)

        return table_layout


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
    def receive_matrix(self):

        self.matrix_dialog=QDialog()
        layout = QFormLayout()
        self.row_lineedit=QLineEdit()
        self.col_lineedit=QLineEdit()
        self.matrix_data=QLineEdit()
        layout.addRow(QLabel("矩阵行:"),self.row_lineedit)
        layout.addRow(QLabel("矩阵列:"), self.col_lineedit)
        layout.addRow(QLabel("以空格隔开输入矩阵:"), self.matrix_data)

        bbOkCancel = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        bbOkCancel.button(QDialogButtonBox.Ok).setDefault(True)
        bbOkCancel.accepted.connect(self.onAccepted)
        bbOkCancel.rejected.connect(self.onRejected)

        layout.addWidget(bbOkCancel)


        self.matrix_dialog.setLayout(layout)


        self.matrix_dialog.exec_()
    def onAccepted(self):
        if self.row_lineedit.text()!="" and self.row_lineedit.text()!="":
            R=int(self.row_lineedit.text())
            C=int(self.col_lineedit.text())

            entries = list(map(float, self.matrix_data.text().split()))

        # For printing the matrix
            self.matrix = np.array(entries).reshape(R, C)

            print(self.matrix)
        else:
            print("错误")

    def onRejected(self):
        self.matrix_dialog.close()