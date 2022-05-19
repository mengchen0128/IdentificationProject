import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit

from Nonlinear_detection_discriminant_method.Instant_AmpOmega_Extraction import Instant_AmpOmega_Extraction


class Example_Cubic_Nonlinearity_Identification:

    def Example_Cubic_Nonlinearity_Identification(self):
        tspan = [0, 150]
        y0 = [1, 0]
        gamma=1
        results = solve_ivp(self.MySystem_Nonlinear, tspan, y0, rtol=1e-12, atol=1e-12, args=([gamma]))
        T = results.t
        Y = results.y
        dt=0.001
        t=np.arange(0,150+dt,dt)
        tck1 = interpolate.splrep(T, Y[0], s=0)
        y1 = interpolate.splev(t, tck1, der=0)
        y = np.array(y1, dtype=float)
        fig1=plt.figure('fig1')
        plt.plot(t, y)

        [T,A_Inst,V_Inst,Omega_Inst]=Instant_AmpOmega_Extraction(t,y)

        fig2=plt.figure('fig2')
        plt.scatter(Omega_Inst,A_Inst)
        plt.xlabel(r"$\omega$")
        plt.ylabel("a")


        fig3=plt.figure('fig3')
        plt.scatter(A_Inst,V_Inst)
        plt.xlabel(r"$\omega$")
        plt.ylabel("a")

        Para0 = 0.01
        popt, pcov = curve_fit(self.DecayFeature, A_Inst,V_Inst, p0=Para0)

        Para = popt

        dt1=0.01
        A=np.arange(0,1+dt1,dt1)
        V=self.DecayFeature(Para,A)

        plt.plot(A,V)

        Para1 = [1, 0.5]

        popt, pcov = curve_fit(self.BackboneFeature, A_Inst,Omega_Inst, p0=Para1)

        Para = popt

        W = self.BackboneFeature1(Para, A)

        fig2 = plt.figure('fig2')

        plt.plot(W, A)

        plt.show()
    def MySystem_Nonlinear(self,t, y, gamma):
        mu = 0.02
        omega0 = 1.5
        dydt = [y[1], -2 * mu * y[1] - omega0 **2*y[0]-gamma*y[0]**3]
        return dydt

    def DecayFeature(self,x,Para):
        y = -Para * x
        return y
    def BackboneFeature(self,x,*Para):
        y = Para[0] + 3 * Para[1] / 8 / Para[0] * x ** 2
        return y
    def BackboneFeature1(self,Para,x):
        y = Para[0] + 3 * Para[1] / 8 / Para[0] * x ** 2
        return y
if __name__ == '__main__':
    w=Example_Cubic_Nonlinearity_Identification()
    w.Example_Cubic_Nonlinearity_Identification()