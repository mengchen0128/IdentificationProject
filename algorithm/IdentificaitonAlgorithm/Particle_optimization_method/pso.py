import numpy as np
from pyswarm import pso


def Evaluation_Function(Mu):
    g=abs(Mu[0]-5)+4*abs(Mu[1]+3)
    return g
lb = [1, -5]
ub = [8, -2]

xopt, fopt = pso(Evaluation_Function, lb, ub,maxiter=200, minfunc=1e-3)
print(xopt)