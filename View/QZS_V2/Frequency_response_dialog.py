import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, \
    QSlider, QLabel


class Frequency_response_dialog(QWidget):

    def __init__(self, *args, **kwargs):
        super(Frequency_response_dialog, self).__init__(*args, **kwargs)
        self.init_UI()

    def init_UI(self):

        vbox = QVBoxLayout()

        self.ax = pg.PlotWidget(background="w")

        self.groupBox = QGroupBox("选择激励频率")
        left_layout = QHBoxLayout(self.groupBox)
        self.leftline = QLabel(self)
        self.leftSlider = QSlider(Qt.Horizontal, self)
        self.leftline.setMaximumWidth(120)
        self.leftline.setMinimumWidth(120)
        left_layout.addWidget(self.leftline)
        left_layout.addWidget(self.leftSlider)

        self.leftSlider.valueChanged.connect(self.onLeftChanged)

        vbox.addWidget(self.ax)

        vbox.addWidget(self.groupBox)


        self.setLayout(vbox)


    def onLeftChanged(self, value):
        self.leftline.setText("激励频率:"+str(value))