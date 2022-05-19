import numpy as np

from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout, QPushButton, QHBoxLayout, QTableView
import pyqtgraph as pg

class detection_dialog(QWidget):

    def __init__(self, *args, **kwargs):
        super(detection_dialog, self).__init__(*args, **kwargs)
        self.init_UI()

    def init_UI(self):

        vbox = QVBoxLayout()

        self.ax = pg.PlotWidget(background="w")


        self.listView = QTableView()



        vbox.addWidget(self.ax)

        vbox.addWidget(self.listView)


        self.setLayout(vbox)


