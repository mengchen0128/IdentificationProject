import json
import os.path

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit

BSER_DIR=os.path.dirname(os.path.realpath(__file__))

class ExtraParaDialog_V2(QDialog):
    def __init__(self,*args,**kwargs):
        super(ExtraParaDialog_V2, self).__init__(*args,**kwargs)
        self.filed_dict = {}
        self.init_ui()


    def init_ui(self):

        layout=QVBoxLayout()

        form_data_list=[
            {"title":"StepTol","filed":"StepTol"},
            {"title":"FunTol","filed":"FunTol"},
            {"title":"R","filed":"R"},
            {"title":"NT","filed":"NT"},
            {"title":"ST","filed":"ST"},
            {"title":"C","filed":"C"},
            {"title":"I","filed":"I"},
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


        self.setLayout(layout)

