from math import log2, ceil
from kyber.constants import q
from kyber.utils.round import normal_round
from kyber.entities.polring import PolynomialRing

def compress(pols: list[PolynomialRing], d: int) -> list[PolynomialRing]:
    """
    Reduces every coefficient of every polynomial in the given list
    to range `0...2**d-1` (inclusive).
    """
    result = []
    for pol in pols:
        f = [compress_int(c, d) for c in pol.coefs]
        result.append(PolynomialRing(f))
    return result

def decompress(pol: PolynomialRing, d: int) -> PolynomialRing:
    """
    Multiplies each coefficient of the given polynomial by `q/(2**d)`.
    Each coefficient of the given polynomial must be in range `0...2^d-1` (inclusive).
    """
    return PolynomialRing([decompress_int(c, d) for c in pol.coefs])

def compress_int(x: int, d: int) -> int:
    """
    Performs compression to a single integer
    by reducing it to range `0...2**d-1` (inclusive).
    """
    assert d < ceil(log2(q))
    result = normal_round((2**d / q) * x) % (2**d)
    assert 0 <= result <= 2**d-1
    return result

def decompress_int(x: int, d: int) -> int:
    """
    Performs decompression to a single integer
    by multiplying it by `q/(2**d)`.
    :param x The integer to be decompressed, in range `0...2**d-1` (inclusive).
    """
    assert d < ceil(log2(q))
    if x < 0 or x > 2**d-1:
        raise ValueError()
    result = normal_round((q / 2**d) * x)
    return result
