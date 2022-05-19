from numpy import zeros


def DerivativeTransform(omega,I):

    Lambda = zeros((2 * I + 1, 2 * I + 1))

    for i in range(1, I + 1):
        Lambda[2 * i-1, 2 * i ]= i * omega
        Lambda[2 * i , 2 * i-1]= -i * omega

    return Lambda