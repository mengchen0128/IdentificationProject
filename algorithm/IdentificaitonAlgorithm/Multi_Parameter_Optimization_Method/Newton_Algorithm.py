import matplotlib.pyplot as plt
import numpy as np
from numpy import dot
from numpy.linalg import eig, inv


def MyFun(mu):
    y = mu[0] ** 2 + 4 * mu[1] ** 2
    return y
def D_MyFun(mu):
    #dydm = np.array([[2 * mu[0]], [8 * mu[1]]])
    dydm =np.concatenate(([2 * mu[0]], [8 * mu[1]]))
    return dydm
def DD_MyFun(mu):
    #dydm = np.array([[2 * mu[0]], [8 * mu[1]]])
    ddydm =np.array([[2,0], [0,8]])
    return ddydm

if __name__ == '__main__':
    mu0 = np.array([[2], [0.5]])
    #mu0=np.concatenate((2,0.5))
    alpha = 0.20
    eps = 1e-4
    Fun_Val = MyFun(mu0)
    Para_Mu = mu0
    dydm = D_MyFun(mu0)
    Iter = 0
    while np.linalg.norm(dydm) > eps:
        dydm = D_MyFun(mu0)
        ddydm = DD_MyFun(mu0)
        c2=min(eig(ddydm)[0])
        if c2 > 0:
            mu0 = mu0 - dot(inv(ddydm),dydm)
        else:
            mu0 = mu0 - alpha * dydm
        Para_Mu = np.concatenate((Para_Mu, mu0),1)
        Iter = Iter + 1
        if Iter > 50:
            break
    fig = plt.figure('fig')
    x = np.array([x / 100.0 for x in range(-200, 201, 1)])
    y = np.array([x / 100.0 for x in range(-100, 101, 1)])
    X, Y = np.meshgrid(x, y)
    F = X ** 2 + 4 * Y ** 2
    c = [0,0.1,0.4,0.8,1.6,3.2]
    plt.contourf(X, Y, F, np.sort(c))
    #plt.contour(X, Y, F)

    plt.plot(Para_Mu[0, :], Para_Mu[1, :], 'o-', markerfacecolor='w')
    plt.xlim(-2, 2)
    plt.ylim(-1, 1)
    plt.show()