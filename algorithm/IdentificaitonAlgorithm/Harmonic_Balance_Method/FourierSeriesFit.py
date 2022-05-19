import functools

import numpy as np
from numpy import sin, cos, ones
from scipy.optimize import curve_fit


def FourierSeriesFit(t, y, omega_q, I):
    order = 2 * I + 1
    p0 = [0.1 for _ in range(order)]
    int2 = functools.partial(CurveFun, I=I,omega_q=omega_q)
    popt, pcov = curve_fit(int2, t, y, p0, method='trf')
    return np.transpose([popt])


def CurveFun(t, *Y,  I,omega_q):
    y = Y[0] * ones(len(t))
    for n in range(1, I + 1):
        y = y + Y[2 * n - 1] * sin(n * omega_q * t) + Y[2 * n] * cos(n * omega_q * t)
    return y
