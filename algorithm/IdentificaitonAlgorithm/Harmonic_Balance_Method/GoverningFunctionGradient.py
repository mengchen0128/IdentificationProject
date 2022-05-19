from numpy import sqrt


def GoverningFunctionGradient(t,dxdt,x,f,mu0):
    c = mu0[0]
    k = mu0[1]
    d = mu0[2]
    L = 5
    # aa=2 * dxdt
    # bb= 2 * (2 * sqrt(d ** 2 + x ** 2) - L) / sqrt(d ** 2 + x ** 2) * x
    # cc=2 * k * L * d / (d ** 2 + x ** 2) ** (3 / 2) * x
    Grad_g = [2 * dxdt, 2 * (2 * sqrt(d ** 2 + x ** 2) - L) / sqrt(d ** 2 + x ** 2) * x,
               2 * k * L * d / (d ** 2 + x ** 2) ** (3 / 2) * x]
    #Grad_g= np.append( np.append(aa,bb),cc)
    return Grad_g