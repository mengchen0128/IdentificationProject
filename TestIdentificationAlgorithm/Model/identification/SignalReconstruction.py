import numpy as np
from numpy import ones, sin, cos


def SignalReconstruction(t,omega,X):


    I = int(np.round(len(X[0,:])-1) / 2)

    # 调整维度
    x = X[:, 0:1] * ones(np.shape(t))

    for i in range(1, I + 1):
        x = x + X[:, 2 * i -1: 2 * i] * sin(i * omega * t) + X[:, 2 * i :2 * i+1] * cos(i * omega * t)

    return x
