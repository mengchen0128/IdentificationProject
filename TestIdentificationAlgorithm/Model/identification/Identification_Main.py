import numpy as np
import scipy.io
from matplotlib.pyplot import semilogy
from numpy import ones, zeros, linspace, eye
from numpy.linalg import norm, eig, linalg

from TestIdentificationAlgorithm.Model.identification.DerivativeTransform import DerivativeTransform
from TestIdentificationAlgorithm.Model.identification.FourierSeriesExpansion_Grad_Phy import \
    FourierSeriesExpansion_Grad_Phy
from TestIdentificationAlgorithm.Model.identification.FourierSeriesExpansion_Grad_Psi import \
    FourierSeriesExpansion_Grad_Psi
from TestIdentificationAlgorithm.Model.identification.FourierSeriesExpansion_State import \
    FourierSeriesExpansion_State
from TestIdentificationAlgorithm.Model.identification.GoverningFunction import GoverningFunction
from TestIdentificationAlgorithm.Model.identification.SignalReconstruction import SignalReconstruction

def Identification_Main():

# User defined parameters for identification initialization.
    M=np.array([[1,0],[0,1]])
    zeta = 0.04
    k11 = 2.1
    k12 = 1
    k2 = 1.5
    k3 = 3
    k4 = 0.2
    mu = np.array([zeta,k11,k12,k2,k3,k4])*0.8
    mu_temp = [zeta,k11,k12,k2,k3,k4]

    #mu1=[i * 0.8 for i in mu_temp]
    StepTol = 1e-4
    FunTol = 1e-4
    R = 50

# Load pre-processed data, which consists of a structure with Q structs.
    Mu=mu
    Data = scipy.io.loadmat(r'Preprocessed Data.mat')
    PreData=Data['PreprocessedData']
    k=PreData[0,0][0][0,0]


# Programer may tune the follwoing setting as will

    NT=20 # Number of time-periods.
    S_T=1000 # Time samples in one time-period.
    C=4000



# Do not edit codes under this line
    Q=np.shape(PreData)[1]
    P=len(mu)
    N=np.shape(M)[0]
    #[N,~]=size(M)
    Gamma=ones((3*N*Q,1))
    Phy=zeros((3*N*Q,N*Q))
    Psi=zeros((3*N*Q,P))
    Increment=ones((N*Q+P,1))
    Increment_History=[]
    Iter=0
    while Iter < R and norm(Gamma) > FunTol and norm(Increment) > StepTol:
        for k in range(0, Q):
            t = linspace(0, NT * 2 * np.pi / PreData[0,k][0][0,0], NT * S_T)
            I = int((len(PreData[0,k][1][0,:])  -1) / 2)
            Lambda = DerivativeTransform(PreData[0,k][0][0,0], I)

            x = SignalReconstruction(t, PreData[0,k][0][0,0], PreData[0,k][1])
            dxdt = SignalReconstruction(t, PreData[0,k][0][0,0], (PreData[0,k][1]) @ Lambda)

            g = GoverningFunction(t, dxdt, x, mu)
            G = FourierSeriesExpansion_State(t, g, PreData[0,k][0][0,0], I)


            Gamma1=PreData[0,k][2][:, 0:1]-G[:, 0:1]
            Gamma2=PreData[0,k][2][:, 1:2]+(PreData[0,k][0][0,0]) ** 2 * M @ (PreData[0,k][1][:, 1:2])-G[:, 1:2]
            Gamma3=PreData[0,k][2][:, 2:3]+(PreData[0,k][0][0,0]) ** 2 * M @ (PreData[0,k][1][:, 2:3])-G[:, 2:3]
            Gamma_temp=np.concatenate((Gamma1, Gamma2, Gamma3))


            Gamma[ k  * 3 * N :k  * 3 * N +3*N] =Gamma_temp


            [Phy_s_0, Phy_c_0] = FourierSeriesExpansion_Grad_Phy(t, dxdt, x, mu, PreData[0,k][0][0,0], 0)
            [Psi_s_0, Psi_c_0] = FourierSeriesExpansion_Grad_Psi(t, dxdt, x, mu, PreData[0,k][0][0,0], 0)


            [Phy_s_1, Phy_c_1] = FourierSeriesExpansion_Grad_Phy(t, dxdt, x, mu, PreData[0,k][0][0,0], 1)
            [Psi_s_1, Psi_c_1] = FourierSeriesExpansion_Grad_Psi(t, dxdt, x, mu, PreData[0,k][0][0,0], 1)


            Phy[k  * 3 * N :k  * 3 * N + 3 * N, k  * N :k  * N +N] =np.vstack((Phy_c_0,Phy_s_1,Phy_c_1))
            Psi[k  * 3 * N :k  * 3 * N + 3 * N,:]=np.vstack((Psi_c_0,Psi_s_1,Psi_c_1))



        Iter = Iter + 1


        CoeMat =np.vstack( (np.hstack((Phy.T @  Phy,Phy.T @ Psi ))  ,  np.hstack ((Psi.T @ Phy,Psi.T @ Psi))))


        Lambda_r = eig(CoeMat)[0]

        lambda_max = max(Lambda_r)
        lambda_min = min(Lambda_r)

        lambda_r = max(lambda_max - C * lambda_min, 0) / (C - 1)

        CoeMat = lambda_r * eye(N * Q + P) + CoeMat

        Increment =  linalg.solve(CoeMat, (np.vstack((Phy.T,Psi.T)) @ Gamma))

        # 待完善
        for k in range(1, Q+1):

            PreData[0,k-1][1][:, 0:1]=PreData[0,k-1][1][:, 0:1]+Increment[(k - 1) * N :(k - 1) * N +N]

        mu = mu + Increment[N * Q :N * Q + P].flatten()

        Mu=np.vstack((Mu,mu))

        if Iter == 1:
            Increment_History = Increment
        else:
            Increment_History = np.hstack((Increment_History, Increment))

        result=[Iter, norm(Gamma), norm(Increment), mu]

        print(result)
    print(Mu)
    Iteration = np.arange(1,Iter+1)

    from matplotlib import pyplot as plt

    fig1 = plt.figure('fig1')
    plt.scatter(Iteration, Mu[1:len(Mu),0].flatten(),s=20)

    fig1 = plt.figure('fig1')
    plt.plot(np.arange(0,len(Mu-2)), [0.04]*len(Mu-1),'--',linewidth=2,color='k')
    plt.xlabel("Iteration step")
    plt.ylabel(r"$\zeta$")
    plt.xlim([0,len(Mu)])
    plt.ylim([0,0.08])
    plt.show()

Identification_Main()