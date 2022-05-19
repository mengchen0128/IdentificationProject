import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, pi, exp

fs=8
Ts=1/fs
f0=1.5
t=np.arange(0,1/f0-Ts,Ts)
x=sin(2*pi*f0*t)
N=len(t)
K=round((N+1)/2)

#X=[0]*(2*K-1)
c=np.arange(-(K-1),K,1)
X=np.zeros(2*K-1,dtype = complex)
for k in range(1, 2*K):
    for n in range(1,N+1):
        temp=exp(-1j * 2 * pi * (k - K) * (n - 1) / N)
        temp1=x[n - 1] * temp
        X[k-1] = X[k-1] + temp1
    X[k-1] = X[k-1] / N

plt.stem(c, abs(X), use_line_collection = True)
plt.show()