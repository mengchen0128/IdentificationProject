import numpy as np
from matplotlib import pyplot as plt
from numpy import sin, diff, unwrap, angle, pi
from scipy.signal import hilbert

omega0=0.5*2*pi
alpha=0
fs=512
k=2
dt=1/fs
t=np.arange(0,150+dt,dt)
x=sin(omega0*t)+alpha*sin(k*omega0*t)
fig1=plt.figure('fig1')
plt.plot(t,x,)
plt.xlim(0,6)

y=hilbert(x)
instfreq = diff(unwrap(angle(y)))/dt
fig2=plt.figure('fig2')

plt.plot(t[0:-1],instfreq,'b',label='HT')
plt.plot(np.linspace(0,6),np.linspace(pi,pi),'k--',label='freq-1')
plt.plot(np.linspace(0,6),np.linspace(2*pi,2*pi),'r-.',label='freq-2')
plt.xlim(0,6)
plt.ylim(-4,8)
plt.legend()
plt.show()