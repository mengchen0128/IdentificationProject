import numpy as np
import scipy.io
from numpy import zeros, sqrt
from numpy.linalg import norm


class Example_Gradient_Clean:
    def Example_Gradient_Clean(self):
        mat = scipy.io.loadmat(r'Simulation Data.mat')

        t=mat['t'][0]
        Disp=mat['Disp'][0]
        Velo=mat['Velo'][0]
        Acce=mat['Acce'][0]
        Exci = zeros(len(Disp))
        m = 1
        L = 5
        mu = np.array([[0.2],[2],[3]])
        alpha = 0.03
        StepSize = 10
        Epsilon = 1e-3
        Iter = 1
        Para = np.array([[0],[0],[0],[0],[0]])
        NT = len(t)

        while StepSize > Epsilon:

            Temp = sqrt(mu[2] ** 2 + Disp ** 2)
            Erro = (m * Acce + 2 * mu[0] * Velo + 2 * mu[1] * (2 * Temp - L) / Temp * Disp - Exci)
            Jaco = 2 * np.vstack([Velo,((2*Temp-L)/Temp *Disp),(mu[1] * mu[2] * L / Temp ** 3. * Disp)])
            Grad = Jaco @ np.transpose([Erro]) / NT
            Delta_mu = -alpha * Grad

            #Para =  np.concatenate((Para,np.vstack([Iter,norm(Delta_mu),mu])),1)
            mu = mu + Delta_mu
            Iter = Iter + 1
            StepSize = norm(Delta_mu)
            if Iter > 50:
                break

if __name__ == '__main__':
    w=Example_Gradient_Clean()
    w.Example_Gradient_Clean()

