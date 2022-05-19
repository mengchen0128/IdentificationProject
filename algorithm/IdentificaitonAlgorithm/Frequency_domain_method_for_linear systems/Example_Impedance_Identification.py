import numpy as np
from numpy import zeros, eye, sin, pi, conj, real
from numpy.fft import fft
from numpy.linalg import inv
from scipy import interpolate
from scipy.integrate import solve_ivp


class Example_Impedance_Identification:
    def Example_Impedance_Identification(self):
        y0 = np.array([0,0,0,0])
        tspan = [0, 200]
        results = solve_ivp(self.MyFun, tspan, y0, rtol=1e-4, atol=1e-4, max_step=1e-2)
        T = results.t
        Y = results.y
        dt = 0.01
        t = np.arange(0, 200 + dt, dt)

        NT = len(t)

        # tck1 = interpolate.splrep(T, Y[0], s=0)
        # x1 = interpolate.splev(t, tck1, der=0)

        f = interpolate.interp1d(T, Y[0],kind='cubic')
        x1 = f(t)

        # tck2 = interpolate.splrep(T, Y[1], s=0)
        # x2 = interpolate.splev(t, tck2, der=0)

        f2 = interpolate.interp1d(T, Y[1],kind='cubic')
        x2 = f2(t)

        x=np.vstack((x1,x2))

        f = zeros((2, NT))

        tf = np.arange(0, 80 + dt, dt)

        N_tf = len(tf)

        cc=np.vstack((sin((0.5 + 0.05 * tf) * tf), sin((8 - 0.05 * tf) * tf)))

        f[:, 0: N_tf]=cc

        Disp = np.vstack((fft(x[0,:]),fft(x[1,:]))) / NT * 2
        Forc = np.vstack((fft(f[0,:]),fft(f[1,:])))/ NT * 2
        df = 1 / t[-1]
        N1 = 40
        N2 = 400
        Omeg = (np.arange(N1,N2+1,1) - 1) * df * 2 * pi
        Disp = Disp[:, N1-1: N2]
        Forc = Forc[:, N1-1: N2]
        Velo = np.vstack([1j * Omeg * Disp[0,:],1j * Omeg * Disp[1,:]])
        Acce = np.vstack([-Omeg ** 2. * Disp[0,:],-Omeg ** 2 * Disp[1,:]])
        Y = np.vstack((Acce,Velo,Disp))
        G = Forc

        cc=G @ conj(Y.T)
        dd=inv(Y @ conj(Y.T))
        P = real(cc @ dd)
        print(P)

    def MyFun(self,t,y):

        M = np.array([[1, 0],[0, 2]])
        C = np.array([[0.2, -0.08],[-0.08, 0.24]])
        K =np.array( [[8, -3],[-3, 10]])

        cc=np.concatenate((zeros((2, 2)), eye(2)),1)
        dd=np.concatenate((inv(-M)  @ K, inv(-M ) @ C),1)
        A = np.concatenate((cc,dd),0)
        y= np.transpose([y])

        if t <= 80:

            dydt = A @ y + np.vstack((0,0,sin((0.5 + 0.05 * t) * t),sin((8 - 0.05 * t) * t) / 2))
        else:
            dydt = A @ y

        #dydt=dydt.tolist()
        dydt=[i for j in dydt for i in j]

        return dydt
if __name__ == '__main__':
    w=Example_Impedance_Identification()
    w.Example_Impedance_Identification()