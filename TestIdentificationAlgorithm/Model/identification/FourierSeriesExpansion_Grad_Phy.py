import numpy as np
from numpy import zeros, sin, cos

from TestIdentificationAlgorithm.Model.identification.GoverningGradient_x import GoverningGradient_x

def FourierSeriesExpansion_Grad_Phy(t,dxdt,x,mu,omega,k):

    Grad_x = GoverningGradient_x(t, dxdt, x, mu)

    [N, S] = np.shape(x)
    Phy_s = zeros((N, N))
    Phy_c = zeros((N, N))
    for n in range(1, N + 1):

        BB=sin(k * omega * t.reshape(len(t),1))

        Phy_s[:, n-1:n] = Grad_x[:,(n-1)*S:(n-1)*S+S] @ BB / S * 2

        Phy_c[:, n-1:n] = Grad_x[:,(n-1)*S:(n-1)*S+S] @ cos(k * omega * t.reshape(len(t),1)) / S * 2

    X=[Phy_s,Phy_c]

    return X


