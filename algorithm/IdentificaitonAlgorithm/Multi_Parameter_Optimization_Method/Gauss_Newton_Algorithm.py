import numpy as np
from matplotlib import pyplot as plt
from numpy import sin, cos, dot, zeros
from numpy.linalg import inv


class Gauss_Newton_Algorithm:
    def Gauss_Newton_Algorithm(self):
        T=np.arange(0,20,0.5)
        T=T.reshape(T.shape[0],1)
        Y = np.array([0.1353, 0.1141, 0.7274, 0.9374, 1.3336, 0.8989, 0.5994, 0.3704, -0.0215, -0.4320, -0.8481,
             - 1.1350, -0.9487, -1.0849, -0.7861, -0.0797, 0.0537, 0.4731, 0.9286, 0.9229, 1.1438, 0.8028,
             0.7368, 0.3173, -0.2063, -0.6739, -0.9843, -1.0214, -1.0449, -0.8841, -0.3890, -0.2103, 0.4031,
             0.5123, 1.0050, 0.9123, 0.9921, 0.9339, 0.4243, 0.0420])
        Y=Y.reshape(Y.shape[0],1)
        mu0 =np.array([[1.2], [0.6]])
        alpha = 0.1
        eps = 1e-4
        Para_Mu = mu0
        r0 = self.ErrorFun(T, Y, mu0)
        # r0 = r0.reshape(r0.shape[0], 1)
        Iter = 0
        DeltaStep = 1
        while np.linalg.norm(DeltaStep) > eps:
            J = self.Jacobi_ErrorFun(T, Y, mu0)
            DeltaStep = np.dot(J.T,r0)
            mu0 = mu0 - alpha * dot(inv(np.dot(J.T,J)), DeltaStep)

            r0=self.ErrorFun(T, Y, mu0)
            Para_Mu = np.concatenate((Para_Mu, mu0), 1)
            Iter = Iter + 1
            if Iter > 100:
                break
        fig = plt.figure('fig')
        a =np.arange(0,2+0.01,0.01)
        omeg = np.arange(0,1.5+0.01,0.01)
        Na = len(a)
        No = len(omeg)
        F = zeros((Na, No))
        for i in range(0, Na):
            for k in range(0, No):
                #c1=np.vstack((a[i], omeg[k]))
                r = self.ErrorFun(T, Y, np.vstack((a[i], omeg[k]))  )
                F[i, k] = np.dot(r.T,r)*40
        c1 = [0,0.1,0.2,0.4,0.8,1.6,3.2]
        plt.contourf(omeg,a,F, c1)
        plt.plot(Para_Mu[1, :],Para_Mu[0, :],  'o-',markerfacecolor='w')
        plt.xlim(0,1.5)
        plt.ylim(0,2)
        plt.show()

    def ErrorFun(self,T,Y,Mu):
        a = Mu[0]
        omega = Mu[1]
        r = (Y - a * sin(omega * T)) / len(T)
        return r

    def Jacobi_ErrorFun(self,T,Y,Mu):
        a = Mu[0]
        omega = Mu[1]
        c1=-sin(omega * T)
        c2=-a * cos(omega * T) * T
        J =  np.concatenate((-sin(omega * T), -a * cos(omega * T)* T),1) / len(T)
        return J
if __name__ == '__main__':
    w=Gauss_Newton_Algorithm()
    w.Gauss_Newton_Algorithm()