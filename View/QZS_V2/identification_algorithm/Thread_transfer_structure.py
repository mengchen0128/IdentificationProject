import numpy as np


def Thread_transfer_structure(pre_data):
    PreData = pre_data

    Q = np.shape(PreData)[1]
    Data = [Item() for i in range(Q)]
    for k in range(0, Q):
        omega = PreData[0, k][0][0, 0]
        F = PreData[0, k][2]
        X = PreData[0, k][1]

        Data[k].omega = omega
        Data[k].X = X
        Data[k].F = F
    return Data

class Item():
    def __init__(self):
        self.omega =[]
        self.X = []
        self.F = []