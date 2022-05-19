import numpy as np
from numpy import mean, sort
from numpy.random import rand

mu1 =np.arange(-2, 2 + 0.01, 0.01)
mu2 = np.arange(-1, 1 + 0.01, 0.01)
mu1_r=(rand(100,1)-0.5)*(mu1[-1]-mu1[0])+mean(mu1)
mu2_r=(rand(100,1)-0.5)*(mu2[-1]-mu2[0])+mean(mu2)
Iter=0
while Iter<20:
    F_r = np.abs(mu1_r) + 4 * np.abs(mu2_r)
    max_value = sort(F_r)
    max_index_col = np.argmax(F_r, axis=0)
    Index=F_r[:,0].argsort()


