import numpy as np

def GoverningGradient_x(t,dxdt,x,mu):

    k11 = mu[1]
    k12 = mu[2]
    k2 = mu[3]
    k3 = mu[4]
    k4 = mu[5]

    Grad_x1_1=k11+2*k2*x[0,:]+3*k3*x[0,:]**2+k4 /(1+(x[0,:]-x[1,:])**2)
    Grad_x1_2=-k4 /(1+(x[0,:]-x[1,:])**2)
    Grad_x1 = np.concatenate((Grad_x1_1, Grad_x1_2),0)

    Grad_x2_1=-k4 /(1+(x[1,:]-x[0,:])**2)
    Grad_x2_2=k12-2*k2*x[1,:]+3*k3*x[1,:]**2+k4 /(1+(x[1,:]-x[0,:])**2)

    Grad_x2 = np.concatenate((Grad_x2_1,Grad_x2_2),0)

    Grad_x=np.vstack((Grad_x1,Grad_x2))

    return Grad_x
