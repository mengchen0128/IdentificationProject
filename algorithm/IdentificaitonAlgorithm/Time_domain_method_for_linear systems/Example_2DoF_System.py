import numpy as np
from numpy import sqrt, exp, sin, cos
from numpy.linalg import inv


class Example_2DoF_System:
    def Example_2DoF_System(self):
        Phi =np.array ([[1 / sqrt(3), -2 / sqrt(6)],[ 1 / sqrt(3), 1 / sqrt(6)]])
        Phi_inv = 1 / 3 * np.array([[sqrt(3), 2 * sqrt(3)], [-sqrt(6), sqrt(6)]])
        x0 = np.array([[1],[-1]])
        dx0 = np.array([[-2],[3]])
        u0 = Phi_inv @ x0
        du0 = Phi_inv @ dx0
        v0 = np.concatenate([[(du0[0] + 1 / 200 * u0[0]) / sqrt(1 - 1 / 200 ** 2)] ,
        [(du0[1] + 1 / 80 * u0[1]) / sqrt(5 / 2 - 1 / 80 ** 2)]])
        dt=0.01
        t=np.arange(0,200+dt,dt)

        u =np.concatenate([ [exp(-1 / 200 * t) * (u0[0] * cos(t) + v0[0] * sin(t))],
        [exp(-1 / 80 * t) * (u0[1] * cos(sqrt(5 / 2) * t) + v0[1] * sin(sqrt(5 / 2) * t))]])

        x = Phi @ u

        du =np.concatenate( [[exp(-1 / 200 * t) * ((v0[0] - 1 / 200 * u0[0]) * cos(t) - (u0[0] + 1 / 200 * v0[0]) * sin(t))],
        [exp(-1 / 80 * t) * ((v0[1] * sqrt(5 / 2) - 1 / 80 * u0[1]) * cos(sqrt(5 / 2) * t) - (
                    sqrt(5 / 2) * u0[1] + 1 / 80 * v0[1]) * sin(sqrt(5 / 2) * t))]])

        dx = Phi @ du

        ddu =np.concatenate( [[exp(-1 / 200 * t) * ((1 / 200 ** 2 * u0[0] - 1 / 100 * v0[0] - u0[0]) * cos(t) + (
                    1 / 200 ** 2 * v0[0] + 1 / 100 * u0[0] - v0[0]) * sin(t)) ],

        [exp(-1 / 80 * t) * (
                    (1 / 80 ** 2 * u0[1] - 1 / 40 * sqrt(5 / 2) * v0[1] - 5 / 2 * u0[1]) * cos(sqrt(5 / 2) * t) + (
                        1 / 80 ** 2 * v0[1] + 1 / 40 * sqrt(5 / 2) * u0[1] - 5 / 2 * v0[1]) * sin(sqrt(5 / 2) * t))]])

        ddx = Phi @ ddu

        M = np.array([[1, 0],[0, 2]])
        X = np.concatenate((dx, x), axis=0)
        F = ddx
        P = -M @ F @ X.T @ inv((X @ X.T))
        C = P[:, 0: 2]
        K = P[:, 2: 4]
        print(C)
        print(K)

if __name__ == '__main__':
    w=Example_2DoF_System()
    w.Example_2DoF_System()



