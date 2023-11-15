import numpy as np
from numpy.polynomial.polynomial import Polynomial
from kyber.utils.compression import compress, decompress
from kyber.utils.encoding import encode, decode
from kyber.utils.modulo import polmod
from kyber.constants import n, k, du, dv

class Decrypt:
    def __init__(self, private_key, ciphertext) -> None:
        self._sk = private_key
        self._c = ciphertext
        if len(self._sk) != 32*12*k:
            raise ValueError()
        if len(self._c) != du*k*n//8 + dv*n//8:
            raise ValueError()

    def decrypt(self) -> bytes:
        """
        Decrypts the given ciphertext with the given private key.
        :returns Decrypted 32-bit shared secret
        """

        # split self._sk into chunks of length 32*12 and decode each one of them into a polynomial
        s = np.array([
            decode(self._sk[32*12*i : 32*12*(i+1)], 12) for i in range(len(self._sk)//(32*12))
        ])

        u, v = self._c[:du*k*n//8], self._c[du*k*n//8:]

        u = np.array([
            decode(u[32*du*i : 32*du*(i+1)], du) for i in range(len(u)//(32*du))
        ])
        v = decode(v, dv)

        u = np.array([decompress(pol, du) for pol in u])
        v = decompress(v, dv)

        m: Polynomial = v - np.matmul(s.T, u)
        m = polmod(m)
        m: bytes = encode(compress([m], 1), 1)

        assert len(m) == 32
        return m
