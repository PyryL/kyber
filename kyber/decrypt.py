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

        s = np.array(decode(self._sk, 12))

        u, v = self._c[:du*k*n//8], self._c[du*k*n//8:]

        u = decode(u, du)
        v = decode(v, dv)[0]

        u = np.array([decompress(pol, du) for pol in u])
        v = decompress(v, dv)

        m: Polynomial = v - np.matmul(s.T, u)
        m = polmod(m)
        m: bytes = encode(compress([m], 1), 1)

        assert len(m) == 32
        return m
