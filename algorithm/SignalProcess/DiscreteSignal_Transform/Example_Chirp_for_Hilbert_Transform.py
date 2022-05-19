import numpy as np
from matplotlib import pyplot as plt
from numpy import sin, diff, unwrap, angle
from scipy.signal import hilbert

omega0=50
alpha=0.01
fs=1024
dt=1/fs
t=np.arange(0,150+dt,dt)
x=sin(omega0*t+alpha*t**2)
omega=omega0+2*alpha*t
fig=plt.figure('fig1')

y=hilbert(x)
instfreq = diff(unwrap(angle(y)))/dt
plt.plot(t,omega,'b',linewidth='3',label='True')
plt.plot(t[0:-1],instfreq,'k--',label='Calculated')
plt.ylim(omega0*0.8,(2*t[-1]*alpha+omega0)*1.2)
plt.legend()
plt.show()

