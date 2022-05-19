import numpy
import numpy as np
from matplotlib import pyplot as plt
from numpy import conj
from scipy import interpolate
from scipy.fft import fft
from scipy.integrate import solve_ivp
from scipy.signal import hilbert


def Example_Nonlinearity_Detect_2():
    tspan=[0,100]
    A=10
    y0=[0,0]
    dt=0.01
    #t=np.arange(100,150+dt,dt)
    a = [x / 100.0 for x in range(0, 10001, 1)]
    t=numpy.array(a, dtype=float)
    results = solve_ivp(MySystem_Nonlinear, tspan, y0, rtol=1e-10, atol=1e-10, args=(A,0.5))
    T = results.t
    Y = results.y
    tck1 = interpolate.splrep(T, Y[0], s=0)
    y1 = interpolate.splev(t, tck1, der=0)
    y = numpy.array(y1, dtype=float)
    Para = [A, 0.5]
    f=[0]*len(t)
    for n in range(0, len(t) - 1):
        if t[n]<=Para[1]:
            f[n] = Para[0] * np.sin(np.pi * t[n] / Para[1])
    H1 =fft(y)
    H2 =fft(np.array(f,dtype=float))
    H = H1 / H2
    HH=1j*np.imag(hilbert(np.real(H)))+np.imag(hilbert(np.imag(H)))
    Lambda = abs(np.real(HH * conj(H)) / (abs(HH) * abs(H)))
    N_Freq = 100
    Omega = (np.array(list(range(1,N_Freq+1)))-1 ) / t[-1] * 2 * np.pi
    plt.ylim(ymax=1, ymin=0)
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\lambda$")
    plt.plot(Omega, Lambda[0:N_Freq],linestyle='', marker='.')
    plt.show()

def MySystem_Nonlinear(t, y, Para1, Para2):
        m = 1
        c = 0.1
        k = 5
        L = 5
        d = 5
        A = Para1
        Width = Para2
        if t <= Width:
            dydt = [y[1],
                -2 * c * y[1] - 2 * k * (2 - L / d + L / (2 * d) * (y[0] / d) ** 2) * y[0] + A * np.sin(np.pi * t/Width) / m]
        else:
            dydt = [y[1],
                -2 * c * y[1] - 2 * k * (2 - L / d + L / (2 * d) * (y[0] / d) ** 2) * y[0]]
        return dydt

if __name__ == '__main__':
    Example_Nonlinearity_Detect_2()