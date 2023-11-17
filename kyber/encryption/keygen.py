from random import randbytes
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from kyber.constants import k, eta1
from kyber.utils.pseudo_random import prf, G, xof
from kyber.utils.cbd import cbd
from kyber.utils.modulo import matmod, polmod
from kyber.utils.byte_conversion import int_to_bytes
from kyber.utils.encoding import encode
from kyber.utils.parse import parse

def generate_keys() -> tuple:
    """
    Generates a new Kyber keypair.
    :returns (private_key, public_key)
    """

    d = randbytes(32)
    rho, sigma = G(d)[:32], G(d)[32:]

    A = np.empty((k, k), Polynomial)
    for i in range(k):
        for j in range(k):
            A[i][j] = parse(xof(rho, int_to_bytes(i), int_to_bytes(j)))

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

    t = np.matmul(A, s) + e     # t is a polynomial matrix with shape (k, )
    t = matmod(t)

    s: bytes = encode(s, 12)
    t: bytes = encode(t, 12)
    assert len(s) == 32*12*k
    assert len(t) == 32*12*k

    return (
        s,          # private key
        t+rho       # public key
    )
