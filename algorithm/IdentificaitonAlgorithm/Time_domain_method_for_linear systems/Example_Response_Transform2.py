import numpy as np
import scipy.io
from numpy import mean, zeros, linalg
from scipy import integrate
from scipy.signal import buttord, butter
from scipy.signal import lfilter


class Example_Response_Transform2:
    def Example_Response_Transform2(self):

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
        t=t.reshape(len(t),-1)
        x = x[:, 2000: ].T
        dx = dx[:, 2000: ].T
        ddx = ddx[:, 2000: ].T
        F = F[:, 2000: ].T
        x_Int = x_Int[:, 2000: ].T
        dx_Int = dx_Int[:, 2000: ].T
        z0 = zeros(len(ddx[:, 0]))
        z0=z0.reshape(len(z0),-1)
        cc=ddx[:,0]


        #a=np.concatenate(([ddx[:, 0]], [z0[:, 0]], [dx_Int[:, 0]], [-dx_Int[:, 1]], [z0[:, 0]], [x_Int[:, 0]], [-x_Int[:, 1]], [z0[:, 0]]),0).T
        a = np.concatenate((ddx[:, 0:1], z0[:, 0:1], dx_Int[:, 0:1], -dx_Int[:, 1:2], z0[:, 0:1], x_Int[:, 0:1],
                            -x_Int[:, 1:2], z0[:, 0:1]), 1)

        #b=np.concatenate(([z0[:, 0]], [ddx[:, 1]], [z0[:, 0]], [-dx_Int[:, 0]], [dx_Int[:, 1]], [z0[:, 0]], [-x_Int[:, 0]], [x_Int[:, 1]]),0).T
        b=np.concatenate((z0[:, 0:1], ddx[:, 1:2], z0[:, 0:1], -dx_Int[:, 0:1], dx_Int[:, 1:2], z0[:, 0:1], -x_Int[:, 0:1], x_Int[:, 1:2]),1)


        A=np.vstack((a,b))

        B = np.concatenate((F[:,0], F[:,1]),0)

        P = linalg.lstsq(A, B,rcond=-1)[0]

if __name__ == '__main__':
    w=Example_Response_Transform2()
    w.Example_Response_Transform2()