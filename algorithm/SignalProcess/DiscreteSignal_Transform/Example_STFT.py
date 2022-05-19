import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, floor, zeros
from scipy import signal
from scipy.fft import fft
from scipy.signal.windows import hamming

omega0=6
alpha=0.1
beta=4
fs=512
dt=1/fs
t=np.arange(0,100+dt,dt)
x=sin(omega0*t+beta/alpha*sin(alpha*t))
omega=omega0+beta*cos(alpha*t)
fig=plt.figure('fig1')
plt.plot(t,x)

N_window=16*fs
N_overlap=round(0.9*N_window)
N_frequency=int(N_window/2)
N_time=int(floor((len(t)-N_overlap)/(N_window-N_overlap)))
S=zeros((N_frequency,N_time))
Freq=np.arange(0,fs/2-fs/N_window,fs/N_window)
Time=zeros(N_time)
w=hamming(N_window).T
F,T,S = signal.stft(x, fs=fs, window=w,nperseg=2*N_frequency,noverlap=N_overlap)
s1= fft(x)
fig1=plt.figure('fig2')
c=np.abs(S)
plt.pcolormesh(T, F, np.abs(S))
plt.xlim(T[0],T[-1])
plt.ylim(0,2)
plt.show()

