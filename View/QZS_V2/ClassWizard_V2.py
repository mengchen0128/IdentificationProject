import os

import scipy.io
from PyQt5.QtWidgets import QWizard, QLabel, QVBoxLayout, QWizardPage, QGroupBox, QGridLayout, QMessageBox

from View.QZS_V2.Estimate_parameters import Estimate_parameters
from View.QZS_V2.Experiment_data_Dialog_V2 import Experiment_data_Dialog_V2
from View.QZS_V2.Extra_parameters_dialog_V2 import ExtraParaDialog_V2
from View.QZS_V2.Governfun_input_V2 import governfun_input_V2
from View.QZS_V2.mixins import MainMixin

BSER_DIR=os.path.dirname(os.path.realpath(__file__))

class ClassWizard_V2(QWizard,MainMixin):
    def __init__(self, parent=None):
        super(ClassWizard_V2, self).__init__(parent)
        self.para_page=ParaInfo_Page()
        self.file_page=FileInfo_Page()
        self.extra_para_page=Extra_para_dialog()
        self.govern_page=GoverningFunction_Page()
        self.govern_mu_page=GoverningGradient_mu_dialog()
        self.govern_x_page=GoverningGradient_x_dialog()
        self.addPage(IntroPage())
        self.addPage(self.para_page)
        self.addPage(self.file_page)
        self.addPage(self.extra_para_page)
        self.addPage(self.govern_page)
        self.addPage(self.govern_mu_page)
        self.addPage(self.govern_x_page)
        self.addPage(ConclusionPage())

        self.registerComponent('para_page',self.para_page)
        self.registerComponent('file_page',self.file_page)
        self.registerComponent('extra_para_page',self.extra_para_page)
        self.registerComponent('govern_page',self.govern_page)
        self.registerComponent('govern_mu_page',self.govern_mu_page)
        self.registerComponent('govern_x_page',self.govern_x_page)



        self.setWindowTitle("请按流程完成数据输入")
        self.resize(600,500)
        self.setAcceptDrops(True)

        self.correct=True
    def extra_save(self):
        """保存额外的参数"""
        data_dict = {}
        for key, filed in self.components['extra_para_page'].extra_para_dialog.filed_dict.items():
            value = filed.text().strip()
            if not value:
                QMessageBox.warning(self, "警告", "参数值不完整")
                self.correct=False
                return

            data_dict[key] = value

        import os
        import json
        file_object = open(os.path.join(BSER_DIR, "database/extra_parameters.json"), mode='w', encoding='utf-8')
        json.dump(data_dict, file_object)
        file_object.close()

    def save_para(self):
        """保存预估参数"""
        data_dict = [[
            "" for _ in range(self.components['para_page'].para_log.table.columnCount())
        ] for _ in range(self.components['para_page'].para_log.table.rowCount())]

        for row in range(self.components['para_page'].para_log.table.rowCount()):
            for col in range(self.components['para_page'].para_log.table.columnCount()):
                it = self.components['para_page'].para_log.table.item(row, col)
                if it and it.text():
                    data_dict[row][col] = self.components['para_page'].para_log.table.item(row, col).text().strip()
                else:
                    QMessageBox.warning(self, "警告", "参数值不能为空或有空行！")
                    self.correct=False
                    return

        import os
        import json
        file_object = open(os.path.join(BSER_DIR, "database/parameters.json"), mode='w', encoding='utf-8')
        json.dump(data_dict, file_object)
        file_object.close()
        self.correct=True


    def output_data(self):
        if self.components['file_page'].experiment_dialog.fileName=="":
            QMessageBox.warning(self, "警告", "请输入文件！")
        else:
            Data = scipy.io.loadmat(self.components['file_page'].experiment_dialog.fileName)
            PreData = Data['PreprocessedData']

            self.components['file_page'].experiment_dialog.input_data.emit(PreData)
    def accept(self):

        self.save_para()
        if self.correct == True:
            self.extra_save()
        else:
            return
        if self.correct == True:

            self.output_data()
        else:
            return
        finish_str = "---数据输入及参数设置完成---"
        self.components['para_page'].para_log.signal_finish.emit(finish_str)
        super(ClassWizard_V2, self).accept()

class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle("引导页")


        self.label = QLabel("请按步骤输入数据,输入控制方程需要对python语法有一定了解，<u>如需帮助请先查看帮助文档！</u>")
        self.label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)


class ParaInfo_Page(QWizardPage):
    def __init__(self, parent=None):
        super(ParaInfo_Page, self).__init__(parent)
        self.init_ui()
    def init_ui(self):
        self.setTitle("参数输入")
        groupBox = QGroupBox()
        groupBoxLayout = QVBoxLayout()

        self.para_log=Estimate_parameters()


        groupBoxLayout.addWidget(self.para_log)

        groupBox.setLayout(groupBoxLayout)


        layout = QVBoxLayout()
        layout.addWidget(groupBox)
        self.setLayout(layout)

class FileInfo_Page(QWizardPage):
    def __init__(self, parent=None):
        super(FileInfo_Page, self).__init__(parent)
        self.init_ui()
    def init_ui(self):
        self.setTitle("将文件拖到下图或者直接打开文件")
        groupBox = QGroupBox()
        groupBoxLayout = QVBoxLayout()

        self.experiment_dialog=Experiment_data_Dialog_V2()

        groupBoxLayout.addWidget(self.experiment_dialog)

        groupBox.setLayout(groupBoxLayout)

        layout = QVBoxLayout()

        layout.addWidget(groupBox)
        self.setLayout(layout)




class Extra_para_dialog(QWizardPage):
    def __init__(self, parent=None):
        super(Extra_para_dialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setTitle("额外的参数")
        groupBox = QGroupBox()
        groupBoxLayout = QVBoxLayout()

        self.extra_para_dialog=ExtraParaDialog_V2()

        groupBoxLayout.addWidget(self.extra_para_dialog)

        groupBox.setLayout(groupBoxLayout)


        layout = QVBoxLayout()
        layout.addWidget(groupBox)
        self.setLayout(layout)


class GoverningFunction_Page(QWizardPage):
    def __init__(self, parent=None):
        super(GoverningFunction_Page, self).__init__(parent)

        self.setTitle("GoverningFunction")
        # self.setSubTitle("Specify basic information about the class for "
        #         "which you want to generate skeleton source code files.")

        groupBox = QGroupBox()
        groupBoxLayout = QVBoxLayout()

        #text_govern=notepad()
        governing_function_textedit = governfun_input_V2(0)


        groupBoxLayout.addWidget(governing_function_textedit)

        groupBox.setLayout(groupBoxLayout)

        layout = QGridLayout()
        layout.addWidget(groupBox, 0, 0)



        self.setLayout(layout)




class GoverningGradient_mu_dialog(QWizardPage):
    def __init__(self, parent=None):
        super(GoverningGradient_mu_dialog, self).__init__(parent)

        self.setTitle("GoverningGradient_mu")
        #self.setSubTitle("Choose the formatting of the generated code.")

        groupBox = QGroupBox()
        groupBoxLayout = QVBoxLayout()

        text_govern_mu = governfun_input_V2(1)
        governing_gradient_mu_textedit = text_govern_mu


        groupBoxLayout.addWidget(governing_gradient_mu_textedit)

        groupBox.setLayout(groupBoxLayout)

        layout = QGridLayout()
        layout.addWidget(groupBox, 0, 0)


        self.setLayout(layout)




class GoverningGradient_x_dialog(QWizardPage):
    def __init__(self, parent=None):
        super(GoverningGradient_x_dialog, self).__init__(parent)

        self.setTitle("GoverningGradient_x")
        # self.setSubTitle("Specify where you want the wizard to put the "
        #         "generated skeleton code.")

        groupBox = QGroupBox()
        groupBoxLayout = QVBoxLayout()

        text_govern_x = governfun_input_V2(2)
        governing_gradient_x_textedit = text_govern_x

        groupBoxLayout.addWidget(governing_gradient_x_textedit)

        groupBox.setLayout(groupBoxLayout)

        layout = QGridLayout()
        layout.addWidget(groupBox, 0, 0)


        self.setLayout(layout)



class ConclusionPage(QWizardPage):
    def __init__(self, parent=None):
        super(ConclusionPage, self).__init__(parent)

        self.setTitle("输入完成")

        self.label = QLabel()
        self.label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def initializePage(self):
        finishText = self.wizard().buttonText(QWizard.FinishButton)
        finishText.replace('&', '')
        self.label.setText("点击 %s 到主界面." % finishText)