import numpy as np
import scipy.io
from numpy import zeros, sqrt
from numpy.random import rand


class Example_PSO_Clean:

    global Acce, Velo, Disp, Exci, NT, L, m
    L = 5
    m = 1
    mat = scipy.io.loadmat(r'Simulation Data.mat')

    t = np.transpose([mat['t'][0]])
    NT = len(t)
    Disp = np.transpose([mat['Disp'][0]])
    Velo = np.transpose([mat['Velo'][0]])
    Acce = np.transpose([mat['Acce'][0]])
    Exci = zeros(Disp.shape)

    def Example_PSO_Clean(self):

        Q = 1000
        w = 0.7
        c1 = 0.3
        c2 = 0.6

        Lambda = np.array([[0.2, 0, 0],[0, 5, 0],[0, 0, 6]])
        b = np.array([[0.1],[4.5],[5]])
        Mu = Lambda @ rand(3, Q) + b
        v = zeros((3, Q))
        Mu_p = zeros((3, Q))
        Mu_q = zeros((3, 1))
        Mu_q1 = zeros((3, Q))
        Generation = 0

        while  Generation < 30:
            g = zeros((Q, 1))
            for q in range(0,Q):
                g[q] = self.Evaluation_Function(Mu[:, q])
                g_Mu = self.Evaluation_Function(Mu_p[:, q])
                if g[q] > g_Mu:
                    Mu_p[:, q]=Mu[:, q]
            [g_max, Index] = [max(g),np.argmax(g)]
            if g_max > self.Evaluation_Function(Mu_q):
                Mu_q = Mu[:, Index]
            r = rand(2, 1)

            Mu_q1[:,0]=Mu_q
            v = w * v + c1 * r[0] * (Mu_p - Mu) + c2 * r[1] * (Mu_q1 - Mu)
            Mu = Mu + v
            Generation = Generation + 1


    def Evaluation_Function(self,mu):
        Temp = sqrt(mu[2] ** 2 + Disp ** 2)
        Erro = (m * Acce + 2 * mu[0] * Velo + 2 * mu[1] * (2 * Temp - L) / Temp * Disp - Exci)
        g = -np.transpose(Erro) @ Erro/(2*NT)
        return g

if __name__ == '__main__':
    w=Example_PSO_Clean()
    w.Example_PSO_Clean()