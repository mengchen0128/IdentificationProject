import numpy as np
from numpy import sin, cos


def Curve_Fitting():
    T = np.arange(0,19.5+0.5,0.5)
    Y = np.array([0.1353, 0.1141, 0.7274, 0.9374, 1.3336, 0.8989, 0.5994, 0.3704, -0.0215, -0.4320, -0.8481,
         - 1.1350, -0.9487, -1.0849, -0.7861, -0.0797, 0.0537, 0.4731, 0.9286, 0.9229, 1.1438, 0.8028,
         0.7368, 0.3173, -0.2063, -0.6739, -0.9843, -1.0214, -1.0449, -0.8841, -0.3890, -0.2103, 0.4031,
         0.5123, 1.0050, 0.9123, 0.9921, 0.9339, 0.4243, 0.0420])
    omega = 0.6
    alpha = 0.05
    eps = 1e-4
    df = D_MyFun(omega, T, Y)
    Iter = 0
    while alpha * abs(df) > eps:
        df = D_MyFun(omega, T, Y)
        ddf = DD_MyFun(omega, T, Y)
        if ddf > 0:
            omega = -(df - omega * ddf) / ddf
        else:
            omega = omega - alpha * df

        Iter = Iter + 1
        if Iter > 2:
            break
    print(omega)



def MyFun(omega,T,Y):
    f=sum((Y-sin(omega*T))**2)/len(T)
    return f
def D_MyFun(omega,T,Y):
    df=-2*sum(T*(Y-sin(omega*T))*cos(omega*T))/len(T)
    return df
def DD_MyFun(omega,T,Y):
    ddf=2*sum(T**2*(cos(omega*T)**2+(Y-sin(omega*T))*sin(omega*T)))/len(T)
    return ddf
Curve_Fitting()
