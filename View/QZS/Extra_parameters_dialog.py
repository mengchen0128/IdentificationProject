import json
import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

BSER_DIR=os.path.dirname(os.path.realpath(__file__))

class ExtraParaDialog(QDialog):
    def __init__(self,*args,**kwargs):
        super(ExtraParaDialog, self).__init__(*args,**kwargs)
        self.filed_dict = {}
        self.init_ui()


    def init_ui(self):

        self.setWindowTitle("额外的参数设置")
        self.resize(300,350)

        layout=QVBoxLayout()

        form_data_list=[
            {"title":"StepTol","filed":"StepTol"},
            {"title":"FunTol","filed":"FunTol"},
            {"title":"R","filed":"R"},
            {"title":"NT","filed":"NT"},
            {"title":"ST","filed":"ST"},
            {"title":"C","filed":"C"},
        ]
        data_dict={}
        alert_file_path=os.path.join(BSER_DIR,"database/extra_parameters.json")
        if os.path.exists(alert_file_path):
            file_object=open(os.path.join(BSER_DIR,"database/extra_parameters.json"), mode='r', encoding='utf-8')
            data_dict=json.load(file_object)

            file_object.close()


        for item in form_data_list:
            label=QLabel()
            label.setText(item['title'])
            layout.addWidget(label)
            txt=QLineEdit()
            filed=item['filed']
            if data_dict and filed in data_dict:
                txt.setText(data_dict[filed])
            layout.addWidget(txt)

            self.filed_dict[item['filed']]=txt

        btn_save=QPushButton("保存")

        btn_save.clicked.connect(self.event_save_click)

        layout.addWidget(btn_save,0,Qt.AlignRight)

        layout.addStretch()

        self.setLayout(layout)


    def event_save_click(self):

        data_dict={}
        for key,filed in self.filed_dict.items():
            value=filed.text().strip()
            if not value:
                QMessageBox.warning(self,"错误","无值")

                return

            data_dict[key]=value

        import os
        import json
        file_object=open(os.path.join(BSER_DIR,"database/extra_parameters.json"), mode='w', encoding='utf-8')
        json.dump(data_dict,file_object)
        file_object.close()


        self.close()