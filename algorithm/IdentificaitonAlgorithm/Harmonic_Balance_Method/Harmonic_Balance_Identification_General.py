import numpy
import numpy as np
from matplotlib import pyplot as plt
from numpy import zeros, pi, sin, eye, sqrt
from numpy.linalg import norm, inv
from scipy import interpolate
from scipy.integrate import solve_ivp

from algorithm.IdentificaitonAlgorithm.Harmonic_Balance_Method.DerivativeMatrix import DerivativeMatrix
from algorithm.IdentificaitonAlgorithm.Harmonic_Balance_Method.FourierSeriesExpansion import FourierSeriesExapansion
from algorithm.IdentificaitonAlgorithm.Harmonic_Balance_Method.GoverningFunction import GoverningFunction
from algorithm.IdentificaitonAlgorithm.Harmonic_Balance_Method.GoverningFunctionGradient import \
    GoverningFunctionGradient
from algorithm.IdentificaitonAlgorithm.Harmonic_Balance_Method.H_Extraction import H_Extraction
from algorithm.IdentificaitonAlgorithm.Harmonic_Balance_Method.Item import Item


def Harmonic_Balance_Identification_General():
    omega_q = np.array([1.0, 1.3, 1.6], dtype=float)
    N_omeg = len(omega_q)
    dt = 0.001
    NT = 20
    y0 = [0, 0]
    Data = [Item() for i in range(N_omeg)]

    for q in range(0, N_omeg):
        tspan = [0, 2 * pi / omega_q[q] * (50 + NT)]
        results = solve_ivp(Nonlinear_System, tspan, y0, rtol=1e-4, atol=1e-4, max_step=1e-2, args=[omega_q[q]])
        T = results.t
        Y = results.y
        t = np.arange((2 * pi / omega_q[q] * 50), (2 * pi / omega_q[q] * (50 + NT)), dt)
        f = sin(omega_q[q] * t)
        tck1 = interpolate.splrep(T, Y[0], s=0)
        x1 = interpolate.splev(t, tck1, der=0)
        x = numpy.array(x1, dtype=float)
        tck2 = interpolate.splrep(T, Y[1], s=0)
        x2 = interpolate.splev(t, tck2, der=0)
        dxdt = numpy.array(x2, dtype=float)
        Data[q].t = t
        Data[q].dxdt = dxdt
        Data[q].x = x
        Data[q].f = f
        Data[q].omega = omega_q[q]
    lam = 0.05
    Mu0 = np.array([[0.06], [3], [5]])
    dMu = Mu0
    Tol_dMu = 1e-3
    I = 9
    Mu = Mu0
    Norm_dMu = []
    Iter = 0
    while norm(dMu) > Tol_dMu:
        beta = zeros(((2 * I + 1) * N_omeg, 1))
        A = zeros(((2 * I + 1) * N_omeg, len(Mu0)))
        for q in range(0, N_omeg):
            t = Data[q].t
            dxdt = Data[q].dxdt
            x = Data[q].x
            f = Data[q].f
            omega = Data[q].omega
            X = FourierSeriesExapansion(t, x, omega, I)
            g = GoverningFunction(t, dxdt, x, f, Mu0)
            G = FourierSeriesExapansion(t, g, omega, I)
            Grad_g = np.array(GoverningFunctionGradient(t, dxdt, x, f, Mu0)).T
            H = H_Extraction(t, Grad_g, I, omega)
            Phi = DerivativeMatrix(omega, I)

            A[q * (2 * I + 1):(2 * I + 1) + q * (2 * I + 1), :] = H
            cc = G + np.dot((Phi.T @ Phi.T), X)
            beta[q * (2 * I + 1):(2 * I + 1) + q * (2 * I + 1), :] = cc

        dMu = inv(lam * eye(len(Mu0)) + A.T @ A) @ A.T @ beta
        Norm_dMu = np.append(Norm_dMu, norm(dMu))
        Mu0 = Mu0 - dMu
        Mu = np.concatenate((Mu, Mu0), 1)
        Iter = Iter + 1
        if Iter > 100:
            break
    N_Iter = len(Norm_dMu)
    Iteration = np.arange(1, N_Iter + 1, 1)
    print(N_Iter)
    fig = plt.figure('fig')


def Nonlinear_System(t, y, omega):
    k = 5
    c = 0.1
    d = 3
    L = 5
    dydt = [y[1], -2 * c * y[1] - 2 * k * (2 * sqrt(d ** 2 + y[0] ** 2) - L) / sqrt(d ** 2 + y[0] ** 2) * y[0] + sin(
        omega * t)]
    return dydt


if __name__ == '__main__':
    Harmonic_Balance_Identification_General()
