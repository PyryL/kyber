from secrets import token_bytes
import numpy as np
from kyber.constants import k, eta1
from kyber.utils.pseudo_random import prf, G, xof
from kyber.utils.cbd import cbd
from kyber.utils.byte_conversion import int_to_bytes
from kyber.utils.encoding import encode
from kyber.utils.parse import parse
from kyber.entities.polring import PolynomialRing

def generate_keys() -> tuple[bytes, bytes]:
    """
    Generates a new Kyber keypair.
    :returns (private_key, public_key)
    """

    d = token_bytes(32)
    rho, sigma = G(d)[:32], G(d)[32:]

    A = np.empty((k, k), PolynomialRing)
    for i in range(k):
        for j in range(k):
            A[i][j] = parse(xof(rho, int_to_bytes(i), int_to_bytes(j)))

    N = 0
    s = np.empty((k, ), PolynomialRing)
    for i in range(k):
        s[i] = cbd(prf(sigma, int_to_bytes(N)), eta1)
        N += 1

    e = np.empty((k, ), PolynomialRing)
    for i in range(k):
        e[i] = cbd(prf(sigma, int_to_bytes(N)), eta1)
        N += 1

    t = np.matmul(A, s) + e     # t is a polynomial matrix with shape (k, )

    s: bytes = encode(s, 12)
    t: bytes = encode(t, 12)
    assert len(s) == 32*12*k
    assert len(t) == 32*12*k

    return (
        s,          # private key
        t+rho       # public key
    )
