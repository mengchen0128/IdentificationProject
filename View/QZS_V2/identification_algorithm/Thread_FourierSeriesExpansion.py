import numpy as np

from View.QZS_V2.identification_algorithm.FourierSeriesExpansion_State_V2 import FourierSeriesExpansion_State_V2


def  FourierSeriesExpansion_Thread(I,pre_data):
        PreData = pre_data

        Q=np.shape(PreData)[1]
        Data = [Item() for i in range(Q)]
        for k in range(0, Q):
            omega = PreData[0,k][0][0,0]
            t = PreData[0,k][1]
            f = PreData[0,k][3]
            x = PreData[0,k][2]

            X=FourierSeriesExpansion_State_V2(t,x,omega,I)

            X[:, 0]=X[:, 0]*0
            F = FourierSeriesExpansion_State_V2(t, f, omega, I)
            Data[k].omega = omega
            Data[k].X = X
            Data[k].F = F
        return Data


class Item():
    def __init__(self):
        self.omega =[]
        self.X = []
        self.F = []

