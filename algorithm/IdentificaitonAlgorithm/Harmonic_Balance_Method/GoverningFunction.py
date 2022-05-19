from numpy import sqrt


def GoverningFunction(t,dxdt,x,f,mu0):
    c = mu0[0]
    k = mu0[1]
    d = mu0[2]
    L = 5
    g = 2 * c * dxdt + 2 * k * (2 * sqrt(d ** 2 + x ** 2) - L) / sqrt(d ** 2 + x ** 2) * x - f
    return g
