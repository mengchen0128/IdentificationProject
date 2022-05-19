import numpy as np
from matplotlib import pyplot as plt
from numpy import cos, eye, sin
from numpy.linalg import eig


class Quasi_Newton_Algorithm:

    def Quasi_Newton_Algorithm(self):
        alpha = 0.1
        eps = 1e-4
        mu0 = np.array([[7], [1]])

        H0 = eye(2)

        dydm0 = self.D_MyFun(mu0)

        mu1 = mu0 - alpha * np.dot(H0 , dydm0)

        dydm1 = self.D_MyFun(mu1)
        s0 = mu1 - mu0
        r0 = dydm1 - dydm0
        Para_Mu = np.concatenate((mu0, mu1),1)
        Index = np.array([0, 0])

        Iter = 0

        while np.linalg.norm(dydm0) > eps:
            H0 = H0 +np.dot( (s0 - np.dot(H0,r0)) , (s0 - np.dot(H0,r0)).T )  /     np.dot((s0-np.dot(H0,r0)).T , r0)

            c2 = min(eig(H0)[0])
            if c2 > 0.1:
                mu0 = mu1
                dydm0 = dydm1
                mu1 = mu0 - alpha * np.dot(H0 , dydm0)
                dydm1 = self.D_MyFun(mu1)
                s0 = mu1 - mu0
                r0 = dydm1 - dydm0
                Index = np.append(Index,1)
            else:
                mu0 = mu1
                dydm0 = dydm1
                mu1 = mu0 - alpha * dydm0
                dydm1 = self.D_MyFun(mu1)
                s0 = mu1 - mu0
                r0 = dydm1 - dydm0
                Index = np.append(Index,0)
            Para_Mu = np.concatenate((Para_Mu, mu1), 1)
            Iter = Iter + 1
            if Iter > 50:
                break
        fig1 = plt.figure('fig')
        x = np.array([x / 100.0 for x in range(100, 1201, 1)])
        y = np.array([x / 100.0 for x in range(100, 501, 1)])
        X, Y = np.meshgrid(x, y)
        F = cos(X)+4*cos(Y)
        c1 = [-5,-4,-3,-2,0]
        c2 =[0,1]
        plt.contourf(X, Y, F, c1)
        #plt.contourf(X, Y, cos(X)*cos(Y), np.sort(c2))
        # plt.contour(X, Y, F)
        # plt.contour(X, Y, cos(X)*cos(Y))
        plt.plot(Para_Mu[0, :], Para_Mu[1, :], 'k--')

        for n in range(0, len(Index)):
            if Index[n] == 0:
                plt.plot(Para_Mu[0, n], Para_Mu[1, n], 'o',markerfacecolor='w')
            else:
                plt.plot(Para_Mu[0, n], Para_Mu[1, n], 'o',markerfacecolor='r')



        plt.xlim(1,12)
        plt.ylim(1,5)
        plt.show()

    def MyFun(self,mu):
        y = cos(mu[0]) + 4 * cos(mu[1])
        return y


    def D_MyFun(self,mu):
        dydm = -np.concatenate(([sin(mu[0])], [4*sin(mu[1])]))
        return dydm
if __name__ == '__main__':
    w=Quasi_Newton_Algorithm()
    w.Quasi_Newton_Algorithm()