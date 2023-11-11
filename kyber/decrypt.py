import numpy as np
from numpy.polynomial.polynomial import Polynomial
from kyber.utils.compression import compress
from kyber.utils.encoding import encode
from kyber.utils.modulo import polmod

class Decrypt:
    def __init__(self, private_key, ciphertext) -> None:
        self._sk = private_key
        self._c = ciphertext

    def decrypt(self) -> bytes:
        """
        Decrypts the given ciphertext with the given private key.
        :returns Decrypted 32-bit shared secret
        """

        s = self._sk
        u, v = self._c

        m: Polynomial = v - np.matmul(s.T, u)
        m = polmod(m)
        m: bytes = encode(compress([m], 1), 1)

        assert len(m) == 32
        return m
