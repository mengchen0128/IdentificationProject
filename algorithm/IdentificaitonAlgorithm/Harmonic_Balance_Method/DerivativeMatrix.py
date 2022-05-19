from numpy import zeros


def DerivativeMatrix(omega, I):
    Phi = zeros((2 * I + 1, 2 * I + 1))
    for n in range(1, I+1):
        Phi[2 * n-1, 2 * n ] = n * omega
        Phi[2 * n , 2 * n-1] = -n * omega
    return Phi
