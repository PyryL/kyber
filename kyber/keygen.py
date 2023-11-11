import numpy as np
from numpy.polynomial.polynomial import Polynomial
from random import randbytes, randint
from kyber.constants import k, eta1, q
from kyber.utils.pseudo_random import prf, G
from kyber.utils.cbd import cbd
from kyber.utils.modulo import matmod, polmod
from kyber.utils.byte_conversion import int_to_bytes

def generate_keys() -> tuple:
    """
    Generates a new Kyber keypair.
    :returns (private_key, public_key)
    """

    d = randbytes(32)
    sigma = G(d)[32:]

    A = np.empty((k, k), Polynomial)
    for i in range(k):
        for j in range(k):
            A[i][j] = Polynomial([randint(0, q-1) for _ in range(256)])

    N = 0
    s = np.empty((k, ), Polynomial)
    for i in range(k):
        s[i] = cbd(prf(sigma, int_to_bytes(N)), eta1)
        s[i] = polmod(s[i])
        N += 1

    e = np.empty((k, ), Polynomial)
    for i in range(k):
        e[i] = cbd(prf(sigma, int_to_bytes(N)), eta1)
        e[i] = polmod(e[i])
        N += 1

    t = np.matmul(A, s) + e
    t = matmod(t)

    return (
        s,          # private key
        (A, t)      # public key
    )
