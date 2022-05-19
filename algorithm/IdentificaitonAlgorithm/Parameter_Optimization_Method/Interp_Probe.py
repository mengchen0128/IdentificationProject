import numpy as np
from numpy import cos, ones, shape
from numpy.linalg import linalg


def Interp_Probe():

    a = 1

    b = 5

    eps = 1e-4

    mu = np.array([[a],[(a + b) / 2],[b]])

    Iter = 0
    while abs(mu[0] - mu[1]) > eps and abs(mu[1] - mu[2]) > eps:

        f = MyFun(mu)


        A = np.hstack((mu ** 2, mu, ones(shape(mu))))

        Coe = linalg.solve(A, f)

        mu_star = -Coe[1] / (2 * Coe[0])

        f_star = MyFun(mu_star)

        Temp_mu = np.vstack((mu,mu_star))

        Temp_f = np.vstack((f,f_star))

        # [~, Index] = sort(Temp_f)
        Index = Temp_f[:, 0].argsort()

        mu = Temp_mu[Index[0:3]]

        Iter = Iter + 1

    print(mu[1])
def MyFun(mu):
    y = cos(mu) + 0.5
    return y
Interp_Probe()