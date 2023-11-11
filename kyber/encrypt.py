import numpy as np
from numpy.polynomial.polynomial import Polynomial
from random import randbytes
from kyber.utils.cbd import cbd
from kyber.utils.pseudo_random import prf
from kyber.utils.modulo import polmod
from kyber.utils.compression import decompress
from kyber.utils.encoding import decode
from kyber.constants import k, eta1, eta2
from kyber.utils.byte_conversion import int_to_bytes

class Encrypt:
    def __init__(self, public_key: bytes) -> None:
        self._pk = public_key
        self._m = randbytes(32)
        self._r = randbytes(32)

    @property
    def secret(self) -> bytes:
        return self._m

    def encrypt(self):
        """
        Encrypts 32-bit random shared secret.
        :returns Ciphertext
        """

        pk = self._pk
        m = self._m
        rb = self._r
        assert len(m) == 32
        assert len(rb) == 32

        A, t = pk

        N = 0
        r = np.empty((k, ), Polynomial)
        for i in range(k):
            r[i] = cbd(prf(rb, int_to_bytes(N)), eta1)
            r[i] = polmod(r[i])
            N += 1

        e1 = np.empty((k, ), Polynomial)
        for i in range(k):
            e1[i] = cbd(prf(rb, int_to_bytes(N)), eta2)
            e1[i] = polmod(e1[i])
            N += 1

        e2 = cbd(prf(rb, int_to_bytes(N)), eta2)
        e2 = polmod(e2)

        u = np.matmul(A.T, r) + e1
        v = np.matmul(t.T, r) + e2 + decompress(decode(m, 1), 1)

        u = [polmod(item) for item in u]
        v = polmod(v)

        return (u, v)
