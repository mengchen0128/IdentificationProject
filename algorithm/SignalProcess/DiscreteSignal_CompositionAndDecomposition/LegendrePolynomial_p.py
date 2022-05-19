
from numpy import  linspace, zeros, sqrt, ones

def LegendrePolynomial_p(I,NT):
    t = linspace(-1, 1, NT)
    s = (I + 1, NT)
    lp = zeros(s)
    s1 = (1, NT)
    lp[0, :] = sqrt(1 / 2) * ones(s1)
    lp[1, :] = sqrt(3 / 2) * t
    for i in range(2, I + 1):
        lp[i, :] = sqrt(2 * (2 * i + 1)) / i * (
                    sqrt((2 * i - 1) / 3) * lp[1, :] * lp[i - 1, :] - (i - 1) / sqrt(2 * i - 3) * lp[0, :] * lp[i - 2,
                                                                                                             :])
    return lp
