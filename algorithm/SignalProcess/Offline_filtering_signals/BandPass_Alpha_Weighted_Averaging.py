import numpy as np
from matplotlib import pyplot as plt
from numpy import pi, zeros, size, cos

alpha1 =0.2
alpha2 =0.4
# fp=0.1*500=50Hz
fs =1000
omega =np.arange(-fs/2 ,fs/ 2 +1 ) * 2 *pi
H= zeros(size(omega))
for n in range(0, len(omega) - 1):
    if  abs(omega[n])>=alpha1*fs*pi and abs(omega[n])<=alpha2*fs*pi:
        H[n] = 1
fig1 = plt.figure('fig1')
plt.plot(omega / 2 / pi, H)
plt.xlim(-fs / 2, fs / 2)
plt.ylim(-0.5, 1.5)

Order = 20
W = zeros(Order + 1)
Hc = zeros(size(omega))
for k in range(0, Order):

    W[k] = np.dot(H, cos(k * omega / fs).T) / fs
    if k == 0:
        Hc = Hc + W[k] * cos(k * omega / fs)
    else:
        Hc = Hc + 2 * W[k] * cos(k * omega / fs)
plt.plot(omega/2/pi,Hc)

plt.show()