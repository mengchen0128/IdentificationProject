import os

import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QGroupBox, QRadioButton, QCheckBox, QPushButton, QDialog, \
    QFileDialog
import xlwt

class result_save_dialog(QDialog):

    def __init__(self,iter_temp,gamma_list_temp,increment_list_temp,mu_result_temp):
        super(result_save_dialog, self).__init__()
        self.iter = iter_temp
        self.gamma_list = gamma_list_temp
        self.increment_list = increment_list_temp
        self.mu=mu_result_temp
        self.init_UI()
    def init_UI(self):

        grid = QGridLayout()
        grid.addWidget(self.createFirstExclusiveGroup(), 0, 0)
        grid.addWidget(self.createNonExclusiveGroup(), 1, 0)
        grid.addWidget(self.createPushButtonGroup(), 1, 1)
        self.setLayout(grid)

        self.setWindowTitle("保存数据")
        self.resize(480, 320)

        self.setLayout(grid)
    def createFirstExclusiveGroup(self):
        groupBox = QGroupBox("选择保存数据的种类")

        radio1 = QRadioButton("&Mat")
        radio2 = QRadioButton("&Excel")

        radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox


    def createNonExclusiveGroup(self):
        groupBox = QGroupBox("选择需要保存的变量")


        checkBox1 = QCheckBox("&Gamma")
        checkBox2 = QCheckBox("&Increment")
        checkBox3 = QCheckBox("&Mu")
        checkBox1.setChecked(True)
        checkBox2.setChecked(True)
        checkBox3.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(checkBox1)
        vbox.addWidget(checkBox2)
        vbox.addWidget(checkBox3)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createPushButtonGroup(self):
        groupBox = QGroupBox("&保存")

        self.popupButton = QPushButton("保存")
        self.popupButton.clicked.connect(self.save_result)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.popupButton)
        groupBox.setLayout(vbox)

        return groupBox
    def save_result(self):
        f = xlwt.Workbook('encoding = utf-8')  # 设置工作簿编码
        sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)  # 创建sheet工作表 # 要写入的列表的值
        for i in range(len(self.iter)):
            sheet1.write(i, 0, self.iter[i])
            sheet1.write(i, 1, self.gamma_list[i])
            sheet1.write(i, 2, self.increment_list[i])

        for i in range(len(self.iter)):
            for j in range(np.shape(self.mu[0])[0]):
                sheet1.write(i, 3+j, self.mu[i].tolist()[j])

                # 写入数据参数对应 行, 列, 值
        filepath, type = QFileDialog.getSaveFileName(self, '文件保存', '/', 'xls(*.xls)')
        if os.path.exists(filepath):
            f.save(filepath)
        else: return
        self.close()
