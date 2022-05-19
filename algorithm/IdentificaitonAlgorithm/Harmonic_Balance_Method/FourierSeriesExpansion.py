from numpy import zeros, mean, sin, cos


def FourierSeriesExpansion(t, y, omega_q, I):
    Y = zeros((2 * I + 1, 1))
    Y[0] = mean(y)
    for n in range(1, I+1):
        Y[2 * n - 1] = mean(y * sin(n * omega_q * t)) * 2
        Y[2 * n] = mean(y * cos(n * omega_q * t)) * 2
    return Y