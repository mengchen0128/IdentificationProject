import numpy as np
import scipy.io
from matplotlib.pyplot import semilogy
from numpy import ones, zeros, linspace, eye
from numpy.linalg import norm, eig, linalg

from TestIdentificationAlgorithm.Model.identification.FourierSeriesExpansion_State import FourierSeriesExpansion_State
from TestIdentificationAlgorithm.Model.identification.Item import Item


def FourierSeriesExpansion(I_temp):
    Data = scipy.io.loadmat(r'Preprocessed Data2.mat')
    PreData = Data['PreprocessedData']
    Q=np.shape(PreData)[1]
    I=I_temp
    Data = [Item() for i in range(Q)]
    for k in range(0, Q):
        omega = PreData[0,k][0][0,0]
        t = PreData[0,k][1]
        f = PreData[0,k][3]
        x = PreData[0,k][2]

        X=FourierSeriesExpansion_State(t,x,omega,I)
        X[:, 0]=X[:, 0]*0
        F = FourierSeriesExpansion_State(t, f, omega, I)
        Data[k].omega = omega
        Data[k].X = X
        Data[k].F = F

    print(type(Data[0].X))
    print(Data[0].F)
    print(Data[20].omega)


FourierSeriesExpansion(11)
