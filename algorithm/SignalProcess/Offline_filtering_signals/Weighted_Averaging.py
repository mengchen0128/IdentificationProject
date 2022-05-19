import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, pi, var, log10


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
    f0=1
    fs=1000
    n=np.arange(0,1000,1)
    x=sin(2*pi*f0*n/fs)
    fig=plt.figure('fig1')
    plt.plot(n/fs,x)

    # target_snr_db = 20
    # # Calculate signal power and convert to dB
    # sig_avg_watts = np.mean(x)
    # sig_avg_db = 10 * np.log10(sig_avg_watts)
    # # Calculate noise according to [2] then convert to watts
    # noise_avg_db = sig_avg_db - target_snr_db
    # noise_avg_watts = 10 ** (noise_avg_db / 10)
    # # Generate an sample of white noise
    # mean_noise = 0
    # noise_volts = np.random.normal(mean_noise, np.sqrt(noise_avg_watts), len(x))
    # y_volts = x + noise_volts
    y=awgn(x,15)+x
    fig2=plt.figure('fig2')
    plt.plot(n/fs,y)

    z = 0.5 * y + 0.25 *  np.append(0,y[0:999])+ 0.25 * np.append(y[1:1000],0)
    np.append(0,y[0:999])
    fig3=plt.figure('fig3')
    plt.plot(n/fs,z)
    print(snr(x, z))

    x1=np.append(y[2:1000],[0,0]) / 6
    u = y / 3 + np.append(0,y[0:999]) / 6 +np.append(y[1:1000],0) / 6 + np.append([0,0],y[0:998]) / 6 + np.append(y[2:1000],[0,0]) / 6
    fig4=plt.figure('fig4')
    print(snr(x,u))

    plt.plot(n/fs,u)

    plt.show()

