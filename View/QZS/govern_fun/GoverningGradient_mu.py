import numpy as np
from numpy import zeros


def GoverningGradient_mu(t, dxdt, x, mu):
    S=len(t)
    a=dxdt[1,:]
    b=x[1,:]
    c=zeros(S)
    d=-x[1, :] ** 2
    e=x[1,:]**3
    f=np.arctan(x[0,:]-x[1,:])
    Grad_mu1 =np.hstack((dxdt[0,:],x[0,:],zeros(S),x[0,:]**2,x[0,:]**3,np.arctan(x[0,:]-x[1,:])))
    Grad_mu2 =np.hstack((dxdt[1,:],zeros(S),x[1,:],-x[1,:]**2,x[1,:]**3,np.arctan(x[1,:]-x[0,:])))

    Grad_mu=np.vstack((Grad_mu1,Grad_mu2))

    return Grad_mu


