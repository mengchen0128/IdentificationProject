import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, zeros, shape, cos, log10
from scipy.signal.windows import blackman


class Example_Windowed_FIR:
    def Example_Windowed_FIR(self):
        alpha1 = 0
        alpha2 = 0.4
        fs = 1000
        omega = np.arange(-fs / 2, fs / 2 + 1, 1) * 2 * pi
        H = zeros(shape(omega))
        for n in range(0, len(omega)):
            if abs(omega[n]) >= alpha1 * fs * pi and abs(omega[n]) <= alpha2 * fs * pi:
                H[n] = 1
        Order = 9
        W = zeros((1, Order + 1))[0]
        Hc = zeros(shape(omega))
        for k in range(0, Order):
            W[k] = (H @ np.transpose(cos(k * omega / fs))) / fs
            if k == 0:
                Hc = Hc + W[k] * cos(k * omega / fs)
            else:
                Hc = Hc + 2 * W[k] * cos(k * omega / fs)

        fig1 = plt.figure('fig1')
        plt.plot(omega / 2 / pi, log10(abs(Hc)) * 20)

        Win = blackman(2 * Order + 1)
        Hc = zeros(shape(omega))

        for k in range(0, Order):
            W[k] = Win[Order + k] * (H @ np.transpose(cos(k * omega / fs))) / fs
            if k == 0:
                Hc = Hc + W[k] * cos(k * omega / fs)
            else:
                Hc = Hc + 2 * W[k] * cos(k * omega / fs)
        plt.plot(omega / 2 / pi, log10(abs(Hc)) * 20)
        plt.xlim([-fs / 2, fs / 2])
        plt.ylim([-60, 10])
        plt.show()


if __name__ == '__main__':
    w = Example_Windowed_FIR()
    w.Example_Windowed_FIR()
