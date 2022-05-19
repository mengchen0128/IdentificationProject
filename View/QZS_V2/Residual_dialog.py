import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class residual_dialog(QWidget):

    def __init__(self,*args,**kwargs):
        super(residual_dialog, self).__init__(*args,**kwargs)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.win=pg.GraphicsLayoutWidget()

        self.win.setBackground('w')
        self.gamma_and_increment()
        layout.addWidget(self.win)

        self.setLayout(layout)


    def gamma_and_increment(self):

        self.gamma_plot = self.win.addPlot(row=0,col=0,title='Gamma residuals')

        self.gamma_plot.showGrid(x=True, y=True)

        self.gamma_plot.setLabel('left', "Gamma")
        self.gamma_plot.setLabel('bottom', "Iter")


        self.increment_plot = self.win.addPlot(row=1,col=0,title='Increment residuals')

        self.increment_plot.showGrid(x=True, y=True)
        self.increment_plot.setLabel('left', "Increment")
        self.increment_plot.setLabel('bottom', "Iter")