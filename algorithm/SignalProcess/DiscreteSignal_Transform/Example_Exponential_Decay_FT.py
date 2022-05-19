import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, exp, cos, zeros

omega=np.arange(0,20+0.01,0.01)
zeta=0.05
omega0=2*pi*0.5
Y=1/2*(1/(zeta+1j*(omega-omega0))+1/(zeta+1j*(omega+omega0)))
fig = plt.figure('fig1')
plt.semilogy(omega/2/pi,abs(Y),label='True')


fs=256
N=100*fs
Ts=1/fs
n=np.arange(0,N,1)
x=exp(-zeta*Ts*n)*cos(omega0*Ts*n)
X=zeros(len(omega),dtype = complex)
for k in range(0, len(omega)):
    X[k]=np.dot(Ts * exp(-1j*omega[k]*n*Ts) , x.T)

plt.semilogy(omega/2/pi,abs(X),label='TF')
plt.legend()

fig2 = plt.figure('fig2')
plt.plot(n*Ts,x)
plt.show()
