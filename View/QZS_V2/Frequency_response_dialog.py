import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, \
    QSlider, QLabel
from numpy import zeros


class Frequency_response_dialog(QWidget):

    def __init__(self, array,*args, **kwargs):
        super(Frequency_response_dialog, self).__init__(*args, **kwargs)
        self.array=array
        self.init_UI()

    def init_UI(self):

        vbox = QVBoxLayout()

        self.ax = pg.PlotWidget(background="w")

        size = np.shape(self.array)[1]

        omega=[]

        X=zeros((2,1))
        for n in range(0,size):

            x=self.array[0, n][2]
            max_amplitude=np.vstack((max(x[0,:]),max(x[1,:])))
            X=np.hstack((X,max_amplitude))
            omega.append(self.array[0, n][0][0,0])

        self.ax.plot(omega,X[0,1:])
        self.ax.plot(omega,X[1,1:])

        vbox.addWidget(self.ax)
        self.setLayout(vbox)


