import functools

import numpy
import numpy as np
from scipy import interpolate
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit


def Example_Nonlinearity_Detect_1():
    tspan=[0,150]
    A=10
    y0=[0,0]
    #Omega=np.arange(0.2,5.2,0.2)
    b=[x / 10.0 for x in range(2, 52, 2)]
    Omega = numpy.array(b, dtype=float)
    N_Ome=len(Omega)
    #Nonlinearity=np.zeros(N_Ome)
    Nonlinearity=[0]*N_Ome
    dt=0.01
    #t=np.arange(100,150+dt,dt)
    a = [x / 100.0 for x in range(10000, 15001, 1)]
    t=numpy.array(a, dtype=float)
    Order1=7
    def MySystem_Nonlinear(t, y, Para1,Para2):
        m = 1
        c = 0.1
        k = 5
        L = 5
        d = 5
        A = Para1
        omega = Para2
        dydt = [y[1], -2 * c * y[1] - 2 * k * (2 - L / d + L / (2 * d) * (y[0] / d) ** 2) * y[0] + A * np.sin(omega * t) / m]
        return dydt
    for n in range(0, N_Ome-1):
        results = solve_ivp(MySystem_Nonlinear, tspan, y0,rtol=1e-10,atol=1e-10,args=(A,Omega[n]))
        T=results.t
        Y=results.y
        tck1 = interpolate.splrep(T, Y[0], s=0)
        y1 = interpolate.splev(t, tck1, der=0)
        y = numpy.array(y1, dtype=float)
        #Para0 = 0.1 * ones(2 * Order, 1)
        order1=2* Order1
        Para0 = [0.1 for _ in range(order1)]
        Para1=[Omega[n],Order1,Para0]
        int2 = functools.partial(CurveFit,omega=Omega[n],Order=Order1)
        popt,pcov  = curve_fit(int2, t, y,Para0)
        Para = popt
        #po=
        P = 0
        # for k in range(1, Order):
        #     P = P + Para[2 * k - 2] ** 2 + Para[2 * k-1] ** 2
        #
        # Nonlinearity[n] = (P - (Para[0] ** 2 + Para[1] ** 2)) / P


def  CurveFit(t,*Para,omega,Order):
     #z=numpy.zeros(len(t))
     m=[0]*len(t)
     z=numpy.array(m,dtype = float)
     l = list(Para)
     #Order=l[1]
     #omega=l[0]
     #temp=l[2:]

     for i in range(1, Order):

         l1=l[2 * i - 2]
         l2=l[2*i-1]
         delta=l1*np.sin(i*omega*t)+l2*np.cos(i*omega*t)
         z=z+delta
     return z

if __name__ == '__main__':
    Example_Nonlinearity_Detect_1()
