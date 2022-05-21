import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QSlider, QLabel
from numpy import zeros


class detection_dialog_V2(QWidget):

    def __init__(self,I,list, *args, **kwargs):
        super(detection_dialog_V2, self).__init__(*args, **kwargs)
        self.list=list
        self.I=I
        self.init_UI()

    def init_UI(self):

        vbox = QVBoxLayout()

        self.ax = pg.plot()

        scatter = pg.PlotWidget()
        self.ax.setYRange(0,1)

        self.ax.setBackground('w')
        Q=len(self.list)

        omega,Nonlinearity=self.cauculate(self.list,Q,self.I)

        vbox.addWidget(self.ax)

        #self.ax.ScatterPlotItem(omega, Nonlinearity[0,:].tolist(),pen=pg.mkPen('b', width=3))
        #scatter.addPoints(omega, Nonlinearity[0,:].tolist())
        #self.ax.addItem(scatter)

        self.ax.plot(omega, Nonlinearity[0,:].tolist(),symbol='o')
        self.setLayout(vbox)

    def cauculate(self,list,length,I):
        Nonlinearity=zeros((2,length))
        omega=[]
        for n in range(0,length):
            X = list[n].X
            omega_temp=list[n].omega
            P = np.array([[0],[0]])
            for k in range(1,I+1):
                P=P+X[:,2*k-2:2*k-1]**2+X[:,2*k-1:2*k]**2
            omega.append(omega_temp)
            Nonlinearity[:,n:n+1]=np.divide((P-(X[:,0:1]**2+X[:,1:2]**2)),P)

        return omega,Nonlinearity

