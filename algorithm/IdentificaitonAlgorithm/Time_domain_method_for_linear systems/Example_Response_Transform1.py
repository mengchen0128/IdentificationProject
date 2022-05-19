import numpy as np
import scipy.io
from numpy import mean
from numpy.linalg import inv
from scipy import integrate
from scipy.signal import buttord, butter
from scipy.signal import lfilter


class Example_Response_Transform1:
    def Example_Response_Transform1(self):

        mat = scipy.io.loadmat(r'Simulated Data.mat')

        t=mat['t'][0]
        x=mat['x'][:,:]
        dx=mat['dx'][:,:]
        ddx=mat['ddx'][:,:]
        F=mat['F'][:,:]


        dx_Int=np.concatenate( ([integrate.cumtrapz(ddx[0,:],t,initial=0)], [integrate.cumtrapz(ddx[1,:],t,initial=0)]))
        dx_Int=np.concatenate(([dx_Int[0,:]-mean(dx_Int[0,:])],[dx_Int[1,:]-mean(dx_Int[1,:])]))

        x_Int=np.concatenate( ([integrate.cumtrapz(dx_Int[0,:],t,initial=0)], [integrate.cumtrapz(dx_Int[1,:],t,initial=0)]))
        x_Int=np.concatenate(([x_Int[0,:]-mean(x_Int[0,:])],[x_Int[1,:]-mean(x_Int[1,:])]))

        fs = 100
        f_pass = np.array([0.4, 40])
        f_stop = np.array([0.2, 45])
        w_pass = f_pass / fs * 2
        w_stop = f_stop / fs * 2
        R_pass = 3
        R_stop = 15

        [N, Wn] = buttord(w_pass, w_stop, R_pass, R_stop)
        [num, den] = butter(N, Wn ,'bandpass')

        ddx = np.concatenate(([lfilter(num,den,ddx[0,:])], [lfilter(num,den,ddx[1,:])]))
        dx = np.concatenate(([lfilter(num,den,dx[0,:])], [lfilter(num,den,dx[1,:])]))
        x = np.concatenate(([lfilter(num,den,x[0,:])], [lfilter(num,den,x[1,:])]))
        dx_Int = np.concatenate(([lfilter(num,den,dx_Int[0,:])], [lfilter(num,den,dx_Int[1,:])]))
        x_Int = np.concatenate(([lfilter(num,den,x_Int[0,:])], [lfilter(num,den,x_Int[1,:])]))
        F = np.concatenate(([lfilter(num,den,F[0,:])], [lfilter(num,den,F[1,:])]))

        t = t[2000:]
        x = x[:, 2000: ]
        dx = dx[:, 2000: ]
        ddx = ddx[:, 2000: ]
        F = F[:, 2000: ]
        x_Int = x_Int[:, 2000: ]
        dx_Int = dx_Int[:, 2000: ]

        X =   np.concatenate((np.concatenate((ddx, dx_Int), axis=0), x_Int), axis=0)
        P =  F @ X.T @ inv((X @ X.T))

        C = P[:, 2: 4]
        M = P[:, 0: 2]
        K = P[:, 4: 6]


if __name__ == '__main__':
    w=Example_Response_Transform1()
    w.Example_Response_Transform1()