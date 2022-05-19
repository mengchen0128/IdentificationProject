import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, zeros, log10, var, sin, ones, real
from scipy.fft import fft, ifft


class BandPass_Alpha_SFFT:

    def awgn(self, x, snr):
        snr = 10 ** (snr / 10.0)
        xpower = np.sum(x ** 2) / len(x)
        npower = xpower / snr
        return np.random.randn(len(x)) * np.sqrt(npower)

    def snr(self, a, b):
        Z = b - a
        residualNoiseDB = 10 * log10(var(Z))
        speechDB = 10 * log10(var(a))
        SNR = speechDB - residualNoiseDB
        return SNR

    def BandPass_Alpha_SFFT(self):
        alpha1 = 0
        alpha2 = 0.05
        fs = 1000
        f0 = 1
        n = np.arange(0, 1000 + 1)
        xr = sin(2 * pi * f0 * n / fs)
        x = self.awgn(xr, 15) + xr
        X = fft(x)
        NX = len(X)
        T = n[-1] / fs
        H = zeros(NX)
        N1 = round(alpha1 * fs / 2 * T) + 1
        N2 = round(alpha2 * fs / 2 * T)
        H[N1 - 1: N2] = ones(N2 - N1 + 1)
        H[(NX - N2): (NX - N1 + 1)] = ones(N2 - N1 + 1)
        X = H * X
        y = real(ifft(X))
        print(self.snr(xr, y))
        plt.xlim(-0.2, 1.2)
        plt.ylim(-1.5, 1.5)
        plt.plot(n / fs, y)

        plt.show()


if __name__ == '__main__':
    w = BandPass_Alpha_SFFT()
    w.BandPass_Alpha_SFFT()
