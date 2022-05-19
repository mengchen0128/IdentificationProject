import matplotlib.pyplot as plt
import numpy as np
omega=np.arange(0,10+0.01,0.01)
zeta=0.05
X=1./(zeta+1j*omega)

fig = plt.figure('fig1')
plt.xlabel('x')
plt.ylabel('y')


plt.semilogy(omega, abs(X))
omega0=3
Y=1/2*(1/(zeta+1j*(omega-omega0))+1/(zeta+1j*(omega+omega0)))

fig2 = plt.figure('fig2')
plt.semilogy(omega,abs(Y))
plt.show()


