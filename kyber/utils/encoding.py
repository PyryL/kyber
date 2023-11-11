import numpy as np
from numpy.polynomial.polynomial import Polynomial
from kyber.utils.byte_conversion import bytes_to_bits, bits_to_bytes

def encode(pols: list[Polynomial], l: int) -> bytes:
    """
    Converts the given polynomial (degree 255, each coefficient in range `0...2**l-1` inclusive)
    into a byte array of lenght `32*l`.
    If multiple polynomials are given, byte arrays are concatenated
    and result length will be `32*l*len(pols)`.
    """

    result = bytearray()
    for pol in pols:
        if len(pol.coef) > 256:
            raise ValueError("too high polynomial degree")
        f = list(pol.coef) + [0 for _ in range(256-len(pol.coef))]
        bits = np.empty((256*l, ))
        for i in range(256):
            f_item = f[i]
            if f_item < 0 or f_item > 2**l-1:
                raise ValueError("invalid polynomial coefficient")
            for j in reversed(range(l)):
                if f_item >= 2**j:
                    bits[i*l+j] = 1
                    f_item -= 2**j
                else:
                    bits[i*l+j] = 0
                assert bits[i*l+j] in [0,1]
            assert f_item == 0
        result += bits_to_bytes(bits)
    assert len(result) == 32*l*len(pols)
    return bytes(result)

def decode(b: bytes, l: int) -> Polynomial:
    """
    Converts the given byte array (length `32*l`) into a polynomial (degree 255)
    in which each coefficient is in range `0...2**l-1` (inclusive).
    """

    if len(b) != 32*l:
        raise ValueError()
    bits = bytes_to_bits(b)
    f = np.empty((256, ))
    for i in range(256):
        f[i] = sum(bits[i*l+j]*2**j for j in range(l))      # accesses each bit exactly once
        assert 0 <= f[i] and f[i] <= 2**l-1
    return Polynomial(f)
