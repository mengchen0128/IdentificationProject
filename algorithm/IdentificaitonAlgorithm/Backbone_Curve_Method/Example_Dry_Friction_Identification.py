from math import atan

import numpy
import numpy as np
from matplotlib import pyplot as plt
from numpy import pi, mean, ones
from scipy import interpolate
from scipy.integrate import solve_ivp

from Nonlinear_detection_discriminant_method.Instant_AmpOmega_Extraction import Instant_AmpOmega_Extraction


class Example_Dry_Friction_Identification:
    def Example_Dry_Friction_Identification(self):
            tspan=[0,100]
            y0=[1,0]
            dt=0.001
            t=np.arange(0,100+dt,dt)
            c = 0.02
            # a = [x / 1000.0 for x in range(0, 100001, 1)]
            # t=numpy.array(a, dtype=float)
            results = solve_ivp(self.MySystem_Nonlinear, tspan, y0, rtol=1e-10, atol=1e-10,max_step=1e-3, args=([c]))
            T = results.t
            Y = results.y
            tck1 = interpolate.splrep(T, Y[0], s=0)
            y1 = interpolate.splev(t, tck1, der=0)
            y = numpy.array(y1, dtype=float)

            fig1 = plt.figure('fig1')
            plt.plot(t, y)


            [T, A_Inst, V_Inst, Omega_Inst] = Instant_AmpOmega_Extraction(t, y)

            fig2 = plt.figure('fig2')
            plt.plot(Omega_Inst,A_Inst,'ro')
            plt.xlim([1.2, 1.8])
            plt.ylim([0.3, 1])

            fig3 = plt.figure('fig3')

            plt.plot(A_Inst,V_Inst,'ro')

            plt.xlim([0.3,1])
            plt.ylim([-0.025,0])

            dt1 = 0.01
            A = np.arange(0, 1 + dt1, dt1)

            Omega_Iden = mean(Omega_Inst)
            W = ones(len(A)) * Omega_Iden

            fig2 = plt.figure('fig2')
            plt.plot(W,A,'k-')

            c_Iden = -mean(V_Inst) * pi * Omega_Iden / 2
            V = -2 * c_Iden / pi / Omega_Iden * ones(len(A))

            fig3 = plt.figure('fig3')

            plt.plot(A,V,'k-')

            plt.show()





    def MySystem_Nonlinear(self,t,y,c):
        omega0 = 1.5
        dydt = [y[1], -c*atan(1000*y[1])/pi*2-omega0**2*y[0]]
        return dydt

if __name__ == '__main__':
    w=Example_Dry_Friction_Identification()
    w.Example_Dry_Friction_Identification()