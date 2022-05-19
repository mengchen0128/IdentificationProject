import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QSlider, QLabel


class detection_dialog_V2(QWidget):

    def __init__(self, *args, **kwargs):
        super(detection_dialog_V2, self).__init__(*args, **kwargs)
        self.init_UI()

    def init_UI(self):

        vbox = QVBoxLayout()

        self.ax = pg.PlotWidget(background="w")

        self.groupBox = QGroupBox("选择激励频率")

        left_layout = QHBoxLayout(self.groupBox)

        self.leftlabel = QLabel(self)
        self.leftSlider = QSlider(Qt.Horizontal, self)
        self.leftlabel.setMinimumWidth(100)
        left_layout.addWidget(self.leftlabel)
        left_layout.addWidget(self.leftSlider)

        self.leftSlider.valueChanged.connect(self.onLeftChanged)

        vbox.addWidget(self.ax)

        vbox.addWidget(self.groupBox)


        self.setLayout(vbox)


    def onLeftChanged(self, value):
        self.leftlabel.setText("激励频率:"+str(value))