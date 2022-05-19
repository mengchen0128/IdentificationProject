import matplotlib.pyplot as plt
import numpy as np

def MyFun(mu):
    y = mu[0] ** 2 + 4 * mu[1] ** 2
    return y
def D_MyFun(mu):
    #dydm = np.array([[2 * mu[0]], [8 * mu[1]]])
    dydm =np.concatenate(([2 * mu[0]], [8 * mu[1]]))
    return dydm

if __name__ == '__main__':
    mu0 = np.array([[2], [0.5]])
    #mu0=np.concatenate((2,0.5))
    alpha = 0.20
    eps = 1e-4
    Fun_Val = MyFun(mu0)
    Para_Mu = mu0
    d0 = -D_MyFun(mu0)
    x1=alpha * d0
    mu1 = mu0 + alpha * d0
    r0 = D_MyFun(mu0)
    Iter = 0
    while np.linalg.norm(r0) > eps:
        r0 = D_MyFun(mu0)
        r1 = D_MyFun(mu1)
        beta0=np.dot(r1.T , (r1 - r0))  /  np.dot(r0.T,r0)
        #beta0 = r1.T*(r1-r0)/(r0.T * r0)
        d1 = -r1 + beta0 * d0
        d0 = d1
        mu0 = mu1
        mu1 = mu0 + alpha * d0
        Para_Mu = np.concatenate((Para_Mu, mu0),1)
        Fun_Val = np.append(Fun_Val, MyFun(mu0))
        Iter = Iter + 1
        if Iter > 50:
            break
    fig=plt.figure('fig')
    x = np.array([x / 100.0 for x in range(-200, 201, 1)])
    y = np.array([x / 100.0 for x in range(-100, 101, 1)])
    X,Y=np.meshgrid(x,y)
    F=X**2 + 4 * Y**2
    c=np.append(0, Fun_Val[1:10])
    plt.contourf(X, Y, F,np.sort(c))
    #plt.contour(X,Y,F)
    plt.plot(Para_Mu[0,:],Para_Mu[1,:],'o-', markerfacecolor='w')
    plt.xlim(-2, 2)
    plt.ylim(-1, 1)
    plt.show()

