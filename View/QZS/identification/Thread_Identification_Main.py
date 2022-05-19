import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from numpy import ones, zeros, linspace, eye, ndarray
from numpy.linalg import norm, eig, linalg

from View.QZS.govern_fun.GoverningFunction import GoverningFunction
from View.QZS.identification.DerivativeTransform import DerivativeTransform
from View.QZS.identification.FourierSeriesExpansion_Grad_Phy import FourierSeriesExpansion_Grad_Phy
from View.QZS.identification.FourierSeriesExpansion_Grad_Psi import FourierSeriesExpansion_Grad_Psi
from View.QZS.identification.FourierSeriesExpansion_State import FourierSeriesExpansion_State
from View.QZS.identification.SignalReconstruction import SignalReconstruction
import ctypes
import win32con

class Thread_Identification_Main(QThread):

    valueChanged = pyqtSignal(list)
    handle=-1
    transfer=pyqtSignal(int,ndarray)

    def __init__(self,mu_temp, PreData_temp, extra_temp,*args,**kwargs):
        super(Thread_Identification_Main, self).__init__(*args,**kwargs)
        self.mu_temp=mu_temp
        self.PreData_temp=PreData_temp
        self.extra_temp=extra_temp


    def run(self):
        try:
            self.handle = ctypes.windll.kernel32.OpenThread(  # @UndefinedVariable
                win32con.PROCESS_ALL_ACCESS, False, int(QThread.currentThreadId()))
        except Exception as e:
            print('get thread handle failed', e)


        # User defined parameters for identification initialization.
        result=[]
        M = np.array([[1, 0], [0, 1]])

        mu = np.array(self.mu_temp)
        Mu = mu
        # mu1=[i * 0.8 for i in mu_temp]
        StepTol = self.extra_temp[0]
        FunTol = self.extra_temp[1]
        R = int(self.extra_temp[2])

        # Load pre-processed data, which consists of a structure with Q structs.

        PreData = self.PreData_temp

        # Programer may tune the follwoing setting as will

        NT = int(self.extra_temp[3])  # Number of time-periods.
        S_T = int(self.extra_temp[4])  # Time samples in one time-period.
        C = int(self.extra_temp[5])

        # Do not edit codes under this line
        Q = np.shape(PreData)[1]
        P = len(mu)
        N = np.shape(M)[0]
        # [N,~]=size(M)
        Gamma = ones((3 * N * Q, 1))
        Phy = zeros((3 * N * Q, N * Q))
        Psi = zeros((3 * N * Q, P))
        Increment = ones((N * Q + P, 1))
        Increment_History = []
        Iter = 0
        while Iter < R and norm(Gamma) > FunTol and norm(Increment) > StepTol:
            for k in range(0, Q):
                t = linspace(0, NT * 2 * np.pi / PreData[0, k][0][0, 0], NT * S_T)
                I = int((len(PreData[0, k][1][0, :]) - 1) / 2)
                Lambda = DerivativeTransform(PreData[0, k][0][0, 0], I)

                x = SignalReconstruction(t, PreData[0, k][0][0, 0], PreData[0, k][1])
                dxdt = SignalReconstruction(t, PreData[0, k][0][0, 0], (PreData[0, k][1]) @ Lambda)

                g = GoverningFunction(t, dxdt, x, mu)
                G = FourierSeriesExpansion_State(t, g, PreData[0, k][0][0, 0], I)

                Gamma1 = PreData[0, k][2][:, 0:1] - G[:, 0:1]
                Gamma2 = PreData[0, k][2][:, 1:2] + (PreData[0, k][0][0, 0]) ** 2 * M @ (PreData[0, k][1][:, 1:2]) - G[:,
                                                                                                                     1:2]
                Gamma3 = PreData[0, k][2][:, 2:3] + (PreData[0, k][0][0, 0]) ** 2 * M @ (PreData[0, k][1][:, 2:3]) - G[:,
                                                                                                                     2:3]
                Gamma_temp = np.concatenate((Gamma1, Gamma2, Gamma3))

                Gamma[k * 3 * N + 0:k * 3 * N + 3 * N] = Gamma_temp

                [Phy_s_0, Phy_c_0] = FourierSeriesExpansion_Grad_Phy(t, dxdt, x, mu, PreData[0, k][0][0, 0], 0)
                [Psi_s_0, Psi_c_0] = FourierSeriesExpansion_Grad_Psi(t, dxdt, x, mu, PreData[0, k][0][0, 0], 0)

                [Phy_s_1, Phy_c_1] = FourierSeriesExpansion_Grad_Phy(t, dxdt, x, mu, PreData[0, k][0][0, 0], 1)
                [Psi_s_1, Psi_c_1] = FourierSeriesExpansion_Grad_Psi(t, dxdt, x, mu, PreData[0, k][0][0, 0], 1)

                Phy[k * 3 * N:k * 3 * N + 3 * N, k * N:k * N + N] = np.vstack((Phy_c_0, Phy_s_1, Phy_c_1))
                Psi[k * 3 * N:k * 3 * N + 3 * N, :] = np.vstack((Psi_c_0, Psi_s_1, Psi_c_1))

            Iter = Iter + 1

            CoeMat = np.vstack((np.hstack((Phy.T @ Phy, Phy.T @ Psi)), np.hstack((Psi.T @ Phy, Psi.T @ Psi))))

            Lambda_r = eig(CoeMat)[0]

            lambda_max = max(Lambda_r)
            lambda_min = min(Lambda_r)

            lambda_r = max(lambda_max - C * lambda_min, 0) / (C - 1)

            CoeMat = lambda_r * eye(N * Q + P) + CoeMat

            Increment = linalg.solve(CoeMat, (np.vstack((Phy.T, Psi.T)) @ Gamma))

            # 待完善
            for k in range(1, Q + 1):
                PreData[0, k - 1][1][:, 0:1] = PreData[0, k - 1][1][:, 0:1] + Increment[(k - 1) * N:(k - 1) * N + N]

            mu = mu + Increment[N * Q:N * Q + P].flatten()
            Mu = np.vstack((Mu, mu))
            if Iter == 1:
                Increment_History = Increment
            else:
                Increment_History = np.hstack((Increment_History, Increment))

            result = [Iter, norm(Gamma), norm(Increment), mu]
            self.valueChanged.emit(result)
        self.transfer.emit(Iter,Mu)





