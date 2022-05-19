import numpy as np

def GoverningFunction(t,dxdt,x,mu):
    zeta = mu[0]
    k11 = mu[1]
    k12 = mu[2]
    k2 = mu[3]
    k3 = mu[4]
    k4 = mu[5]

    g1 = zeta * dxdt[0, :] + k11 * x[0, :] + k2 * x[0, :] ** 2 + k3 * x[0, :] ** 3 + k4 * np.arctan(x[0, :] - x[1, :])
    g2 = zeta * dxdt[1, :] + k12 * x[1, :] - k2 * x[1, :] ** 2 + k3 * x[1, :] ** 3 + k4 * np.arctan(x[1, :] - x[0, :])
    g=np.array((g1,g2))

    return g

