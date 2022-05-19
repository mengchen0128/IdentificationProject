import scipy.io
from numpy import zeros

from SignalProcess.DiscreteSignal_CompositionAndDecomposition.BasisCoefficient_X import BasisCoefficient_X
from SignalProcess.DiscreteSignal_CompositionAndDecomposition.LegendrePolynomial_p import LegendrePolynomial_p


class Example_LP_Reconstruction:
    def Example_LP_Reconstruction(self):
        mat = scipy.io.loadmat(r'Simulation Data Noisy.mat')

        t = mat['t'][0]
        Disp = mat['Disp'][0]

        I = 5
        N_LP = 1001
        T = t[N_LP-1] - t[0]

        lp = LegendrePolynomial_p(I, N_LP)

        X_q = BasisCoefficient_X(Disp[0:N_LP], lp)

    def AuxiliaryFunction_theta(self,I):
        theta = zeros((I + 1, I + 1))
    def DerivativeTrasnformation_Lambda(self,I,T,theta):
        omega = zeros((I + 1, I + 1))



if __name__ == '__main__':
    w=Example_LP_Reconstruction()
    w.Example_LP_Reconstruction()





