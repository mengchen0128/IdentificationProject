import numpy as np
from matplotlib import pyplot as plt
from numpy import sin

from SignalProcess.DiscreteSignal_CompositionAndDecomposition.BasisCoefficient_X import BasisCoefficient_X
from SignalProcess.DiscreteSignal_CompositionAndDecomposition.LegendrePolynomial_p import LegendrePolynomial_p


class Legendre_Polynomial_Decom:




    def Legendre_Polynomial_Decom(self):
        t=np.arange(0,2+0.001,0.001)
        T=2
        x=sin(2*t)+0.5*sin(7*t)
        I=30
        NT=len(t)
        lp=LegendrePolynomial_p(I,NT)
        X_q=BasisCoefficient_X(x,lp)
        y = np.dot(X_q.T,lp)
        fig = plt.figure('fig1')
        plt.plot(t, x)
        fig2 = plt.figure('fig2')
        plt.plot(t,y)
        plt.show()
if __name__ == '__main__':
    w=Legendre_Polynomial_Decom()
    w.Legendre_Polynomial_Decom()
