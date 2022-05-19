import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, zeros, size, cos, log10, var, sin, flip


def awgn(x, snr):
    snr = 10**(snr/10.0)
    xpower = np.sum(x**2)/len(x)
    npower = xpower / snr
    return np.random.randn(len(x)) * np.sqrt(npower)
def snr(a, b):
    Z=b-a
    residualNoiseDB = 10 * log10(var(Z))
    speechDB = 10 * log10(var(a))
    SNR = speechDB - residualNoiseDB
    return SNR
if __name__ == '__main__':
    alpha=0.1
    #fp=0.1*500=50Hz
    fs=1000
    omega=np.arange(-fs/2,fs/2+1)*2*pi
    H=zeros(size(omega))
    for n in range(0,len(omega)-1):
        if abs(omega[n])<=alpha*500*2*pi:
            H[n]=1
    fig1=plt.figure('fig1')
    plt.plot(omega/2/pi,H)
    plt.xlim(-fs/2,fs/2)
    plt.ylim(-0.5,1.5)


    Order=20
    W=zeros(Order+1)
    Hc=zeros(size(omega))
    for k in range(0,Order):
        cc=np.dot(H , cos(k * omega / fs))
        W[k] = np.dot(H , cos(k * omega / fs).T)/fs
        if k == 0:
            Hc=Hc+W[k] * cos(k * omega / fs)
        else:
            Hc = Hc + 2 * W[k] * cos(k * omega / fs)

    plt.plot(omega/2/pi,Hc)
    fig2=plt.figure('fig2')
    hn=np.append(flip(W),W[1:-1])
    f0=1
    n=np.arange(0,1000+1,1)
    x=sin(2*pi*f0*n/fs)
    y=awgn(x,15)+x
    z=np.convolve(y,hn)
    z=z[Order:-(Order-1)]
    snr(x,z)
    plt.plot(n / fs, y)
    plt.plot(n / fs, z)

    plt.xlim(-0.2, 1.2)
    plt.ylim(-1.5, 1.5)
    plt.show()
