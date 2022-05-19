from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QGroupBox, QRadioButton, QCheckBox, QPushButton, QDialog


class result_save_dialog(QDialog):

    def __init__(self):
        super(result_save_dialog, self).__init__()
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

        popupButton = QPushButton("保存")

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(popupButton)
        groupBox.setLayout(vbox)

        return groupBox
