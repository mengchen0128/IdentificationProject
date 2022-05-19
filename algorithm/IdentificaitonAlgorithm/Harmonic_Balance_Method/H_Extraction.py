from numpy import zeros, mean, sin, cos, size


def H_Extraction(t, Grad_g, I, omega_q):
    N_Mu = len(Grad_g[0, :])
    c=size(t)
    # [a, b] = size(t)
    # if a < b:
    #     t = t.T
    H = zeros((2 * I + 1, N_Mu))
    for m in range(0, N_Mu):
        H[0, m] = mean(Grad_g[:, m])
        for n in range(1, I+1):
            H[2 * n-1, m] = mean(Grad_g[:, m] * sin(n * omega_q * t)) * 2
            H[2 * n , m] = mean(Grad_g[:, m] * cos(n * omega_q * t)) * 2
    return H
