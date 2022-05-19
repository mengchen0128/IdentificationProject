import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, exp, cos, zeros

omega=np.arange(-20,20+0.01,0.01)
fs=256
Tw=64
N=Tw*fs
Ts=1/fs
n=np.arange(0,N,1)
x=0.54-0.46*cos(2*pi*n*Ts/Tw)
X=zeros(len(omega),dtype = complex)
for k in range(0, len(omega)):
    X[k]=np.dot(Ts * exp(-1j*omega[k]*n*Ts) , x.T)
fig = plt.figure('fig1')
plt.semilogy(omega/2/pi,abs(X),label='TF')
plt.legend()

fig2 = plt.figure('fig2')
plt.plot(n*Ts,x)
plt.show()