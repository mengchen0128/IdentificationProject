import numpy as np
from numpy import zeros, mean, sin, cos

def FourierSeriesExpansion_State_V2(t,x,omega,I):
    [N, S] = np.shape(x)

    X = zeros((N, 2 * I + 1))

    X[:,0] = mean(x, 1)

    for n in range(1, I + 1):

        X[:,2 * n - 1:2*n] = x @ sin(n * omega * t.T) / S * 2
        X[:,2 * n:2*n+1] = x @ cos(n * omega * t.T) / S * 2

    return X
