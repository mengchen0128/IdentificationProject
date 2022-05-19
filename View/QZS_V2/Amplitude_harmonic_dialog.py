import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QGroupBox


class Amplitude_harmonic_dialog(QWidget):

    def __init__(self,list,*args,**kwargs):
        super(Amplitude_harmonic_dialog, self).__init__(*args,**kwargs)
        self.list=list
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.win=pg.GraphicsLayoutWidget()

        self.win.setBackground('w')
        self.gamma_and_increment()

        self.groupBox = QGroupBox("选择激励频率")
        left_layout = QHBoxLayout(self.groupBox)

        self.leftlabel = QLabel(self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.leftlabel.setMinimumWidth(100)
        left_layout.addWidget(self.leftlabel)
        left_layout.addWidget(self.slider)
        length=len(self.list)-1

        self.slider.setMinimum(0)
        #设置最大值
        self.slider.setMaximum(length)

        self.slider.setSingleStep(3)


        self.slider.valueChanged.connect(self.onLeftChanged)




        layout.addWidget(self.win)

        layout.addWidget(self.groupBox)

        self.setLayout(layout)


    def gamma_and_increment(self):

        self.response = self.win.addPlot(row=0,col=0,title='Harmonic coefficients of response')

        self.response.showGrid(x=True, y=True)

        self.response.setLabel('left', "Amplitude")
        self.response.setLabel('bottom', "omega")


        self.excitation = self.win.addPlot(row=1,col=0,title='Harmonic coefficient of excitation')

        self.excitation.showGrid(x=True, y=True)
        self.excitation.setLabel('left', "Amplitude")
        self.excitation.setLabel('bottom', "omega")


    def onLeftChanged(self, value):
        a=self.list[value].omega
        self.leftlabel.setText("激励频率:"+str(round(a,1)))

        # n=np.shape(self.list[value].X)[1]
        # x=[i for i in range(1,n+1)]

        self.response.plot(self.list[value].X[0,:],pen=pg.mkPen('b', width=3),clear=True)

        self.response.plot(self.list[value].X[1,:],pen=pg.mkPen('r', width=3))


        self.excitation.plot(self.list[value].F[0,:],pen=pg.mkPen('b', width=3),clear=True)
        self.excitation.plot(self.list[value].F[1,:],pen=pg.mkPen('r', width=2))

        pg.QtGui.QApplication.processEvents()


