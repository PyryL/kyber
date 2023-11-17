from random import randbytes
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from kyber.utils.cbd import cbd
from kyber.utils.pseudo_random import prf
from kyber.utils.modulo import matmod, polmod
from kyber.utils.compression import compress, decompress
from kyber.utils.encoding import encode, decode
from kyber.constants import k, eta1, eta2, n, du, dv
from kyber.utils.byte_conversion import int_to_bytes
from kyber.utils.parse import parse
from kyber.utils.pseudo_random import xof

class Encrypt:
    def __init__(self, public_key: bytes, m: bytes = None, r: bytes = None) -> None:
        self._pk = public_key
        self._m = m if m is not None else randbytes(32)
        self._r = r if r is not None else randbytes(32)
        assert len(self._m) == 32
        assert len(self._r) == 32
        if len(self._pk) != 12 * k * int(n/8) + 32:
            raise ValueError()

    @property
    def secret(self) -> bytes:
        """The 32-bit shared secret that was encrypted."""
        return self._m

    def encrypt(self):
        """
        Encrypts 32-bit random shared secret.
        :returns Ciphertext
        """

        m = self._m
        rb = self._r

        t, rho = self._pk[:-32], self._pk[-32:]
        t = np.array(decode(t, 12))

        A = np.empty((k, k), Polynomial)
        for i in range(k):
            for j in range(k):
                A[i][j] = parse(xof(rho, int_to_bytes(i), int_to_bytes(j)))

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
        v = np.matmul(t.T, r) + e2 + decompress(decode(m, 1)[0], 1)

        u = matmod(u)
        v = polmod(v)

        u = compress(u, du)
        v = compress([v], dv)

        u = encode(u, du)
        v = encode(v, dv)

        assert len(u) == du * k * n//8
        assert len(v) == dv * n//8

        return u + v
