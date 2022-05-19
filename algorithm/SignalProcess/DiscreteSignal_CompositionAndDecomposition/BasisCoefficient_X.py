import numpy as np
from numpy.linalg import inv


def BasisCoefficient_X( x, lp):
    # lc=np.array(lp)
    # x1=np.array(x)
    c = np.dot(lp, lp.T)
    X_q = np.dot(inv(np.dot(lp, lp.T)), (np.dot(lp, x.T)))
    return X_q
