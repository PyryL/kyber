import numpy as np
from kyber.utils.compression import compress, decompress
from kyber.utils.encoding import encode, decode
from kyber.constants import n, k, du, dv
from kyber.entities.polring import PolynomialRing

def decrypt(private_key: bytes, ciphertext: bytes) -> bytes:
    """
    Decrypts the given ciphertext with the given private key.
    :returns Decrypted 32-bit shared secret
    """

    if len(private_key) != 32*12*k:
        raise ValueError()
    if len(ciphertext) != du*k*n//8 + dv*n//8:
        raise ValueError()

    s = np.array(decode(private_key, 12))

    u, v = ciphertext[:du*k*n//8], ciphertext[du*k*n//8:]

    u = decode(u, du)
    v = decode(v, dv)[0]

    u = np.array([decompress(pol, du) for pol in u])
    v = decompress(v, dv)

    m: PolynomialRing = v - np.matmul(s.T, u)
    m: bytes = encode(compress([m], 1), 1)

    assert len(m) == 32
    return m
