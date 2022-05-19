import numpy as np
from numpy import zeros, sin, cos

from View.QZS.govern_fun.GoverningGradient_mu import GoverningGradient_mu


def FourierSeriesExpansion_Grad_Psi(t,dxdt,x,mu,omega,k):

    Grad_mu = GoverningGradient_mu(t, dxdt, x, mu)
    P=len(mu)
    [N, S] = np.shape(x)
    Psi_s = zeros((N, P))
    Psi_c = zeros((N, P))
    for n in range(1, P + 1):


        BB=sin(k * omega * t.reshape(len(t),1))

        Psi_s[:, n-1:n] = Grad_mu[:,(n-1)*S:(n-1)*S+S] @ BB / S * 2

        Psi_c[:, n-1:n] = Grad_mu[:,(n-1)*S:(n-1)*S+S] @ cos(k * omega * t.reshape(len(t),1)) / S * 2


    X=[Psi_s,Psi_c]

    return X
