from math import floor
from typing import Generator
import numpy as np
from kyber.constants import n, q
from kyber.entities.polring import PolynomialRing

def byte_to_int(b: bytes) -> int:
    """Returns the unsigned integer that the given big-endian byte array represents."""
    return int.from_bytes(b)

def parse(stream: Generator[bytes, None, None]) -> PolynomialRing:
    """
    Deterministically creates a polynomial (degree n-1, each coefficient in
    range `0...4095` inclusive) from the given bytestream.
    """

    i, j = 0, 0
    a = np.empty((n, ))
    while j < n:
        b1, b2, b3 = byte_to_int(next(stream)), byte_to_int(next(stream)), byte_to_int(next(stream))
        d1 = b1 + 256 * (b2 % 16)
        d2 = floor(b2 / 16) + 16 * b3
        if d1 < q:
            a[j] = d1
            j += 1
        if d2 < q and j < n:
            a[j] = d2
            j += 1
        i += 3
    return PolynomialRing(a)
