import numpy as np
from matplotlib import pyplot as plt
from numpy import pi, exp, cos, ceil, log2
from scipy.fft import fft
#omega=np.arange(0,20.01,0.01)
omega=np.array([x / 100.0 for x in range(0, 2001, 1)])
zeta=0.05
omega0=2*pi*0.5
Y=1/2*(1/(zeta+1j*(omega-omega0))+1/(zeta+1j*(omega+omega0)))
fig1 = plt.figure('fig1')
plt.semilogy(omega/2/pi,abs(Y),label='True')

fs=2**10
N=2**6*fs
Ts=1/fs
n=np.arange(0,N,1)
x=exp(-zeta*Ts*n)*cos(omega0*Ts*n)
Nx = len(x)
M = ceil(log2(Nx))
y = np.zeros(int(2 ** M))
y[0: Nx]=x
df=fs/2**M
Freq=np.arange(0,2**M,1)*df
theta2=fft(y)/fs

plt.semilogy(Freq,abs(theta2),label='Fit')
x1=omega[0]/2/pi
x2=omega[-1]/2/pi
x3=omega[-1]
plt.xlim(omega[0]/2/pi,omega[-1]/2/pi)

plt.legend()
plt.show() 