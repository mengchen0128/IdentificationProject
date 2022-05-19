import numpy as np
from PyQt5.QtWidgets import QMainWindow

from View.Signal_Process.SignalDialogView import ChildDialogUi


class SignalDialogController(QMainWindow,ChildDialogUi):
    def __init__(self, parent=None):
        super(SignalDialogController, self).__init__(parent)
        self.setupUi(self)
        self.button.clicked.connect(self.plot)

    def plot(self):
        freq1 = int(self.lineEdit1.text())
        sample_rate1 = int(self.lineEdit2.text())
        duration1 = int(self.lineEdit3.text())
        x, y = self.generate_sine_wave(freq1, sample_rate1, duration1)

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot()

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(x, y)

        # refresh canvas
        self.canvas.draw()

    def generate_sine_wave(self, freq, sample_rate, duration):
        x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
        print(len(x))
        frequencies = x * freq
        # 2pi because np.sin takes radians
        y = np.sin((2 * np.pi) * frequencies)
        return x, y
