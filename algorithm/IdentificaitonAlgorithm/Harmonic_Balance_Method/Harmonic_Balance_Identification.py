import numpy
import numpy as np
from numpy import zeros, pi, sin, linalg
from scipy import interpolate
from scipy.integrate import solve_ivp

from algorithm.IdentificaitonAlgorithm.Harmonic_Balance_Method.DerivativeMatrix import DerivativeMatrix
from algorithm.IdentificaitonAlgorithm.Harmonic_Balance_Method.FourierSeriesExpansion import FourierSeriesExapansion


def Harmonic_Balance_Identification():
    omega_q = np.array([1.0, 1.3, 1.6], dtype=float)
    N_omeg = len(omega_q)
    I = 5
    A = zeros(((2 * I + 1) * N_omeg, 3))
    b = zeros(((2 * I + 1) * N_omeg, 1))
    dt = 0.001
    NT = 20
    y0 = [0, 0]

    def Nonlinear_System(t, y, omega):
        mu = 0.06
        omega0 = 1.5
        gamma = 1
        dydt = [y[1], -2 * mu * y[1] - omega0 ** 2 * y[0] - gamma * y[0] ** 3 + sin(omega * t)]
        #dydt=np.concatenate(([y[1],[-2 * mu * y[1] - omega0 ** 2 * y[0] - gamma * y[0] ** 3 + sin(omega * t)]]),1)
        return dydt

    for q in range(0, N_omeg):
        tspan = [0, 2 * pi / omega_q[q] * (50 + NT)]
        results = solve_ivp(Nonlinear_System, tspan, y0, rtol=1e-4, atol=1e-4, max_step=1e-2,args=[omega_q[q]])
        T = results.t
        Y = results.y
        t = np.arange((2 * pi / omega_q[q] * 50), (2 * pi / omega_q[q] * (50 + NT)), dt)
        f = sin(omega_q[q] * t)
        tck1 = interpolate.splrep(T, Y[0], s=0)
        x1 = interpolate.splev(t, tck1, der=0)
        x = numpy.array(x1, dtype=float)
        F = FourierSeriesExapansion(t, f, omega_q[q], I)
        X = FourierSeriesExapansion(t, x, omega_q[q], I)
        Y = FourierSeriesExapansion(t, x ** 3, omega_q[q], I)
        Phi = DerivativeMatrix(omega_q[q], I)
        A[q * (2 * I + 1) :(2 * I+1)+q  * (2 * I + 1),:]=np.concatenate((np.concatenate((2 * np.dot(Phi.T,X),X),1),Y),1)
        cc=F - np.dot((Phi.T @ Phi.T), X)
        b[q * (2 * I + 1) :(2 * I+1)+q  * (2 * I + 1),:]=cc
    Para=linalg.lstsq(A, b, rcond=-1)[0]
    print(Para)

if __name__ == '__main__':
    Harmonic_Balance_Identification()
