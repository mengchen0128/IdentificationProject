from numpy import sqrt


def Golden_Probe():
    a = 0
    b = 4
    eps = 1e-4
    alpha = 1 - (sqrt(5) - 1) / 2

    Iter = 0
    Bl = a
    Br = b
    mu_l = Bl + alpha * (Br - Bl)
    mu_r = Br - alpha * (Br - Bl)
    while abs(Br - Bl) > eps:
        if MyFun(mu_l) < MyFun(mu_r):
            Br = mu_r
            mu_r = mu_l
            mu_l = Bl + alpha * (Br - Bl)
        else:
            Bl = mu_l
            mu_l = mu_r
            mu_r = Br - alpha * (Br - Bl)

        Iter = Iter + 1
        print(mu_l)

def MyFun(mu):
    y = (mu - 1.5) ** 2 + 1
    return y
Golden_Probe()