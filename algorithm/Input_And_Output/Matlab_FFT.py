import numpy as np
from numpy import ceil, log2
from scipy.fft import fft


def Matlab_FFT(x,fs):
    Nx = len(x)
    M = ceil(log2(Nx))
    y = np.zeros(int(2 ** M))
    y[0: Nx]=x
    df = fs / 2 ** M
    Freq=np.arange(0,2**M,1)*df
    theta2 = fft(y) / fs
    X = theta2
    return X,Freq