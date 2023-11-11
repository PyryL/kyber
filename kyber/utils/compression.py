from math import log2, ceil
from numpy.polynomial.polynomial import Polynomial
from kyber.constants import q
from kyber.utils.round import normal_round

def compress(pols: list[Polynomial], d: int) -> list[Polynomial]:
    """
    Reduces every coefficient of every polynomial in the given list
    to range `0...2**d-1` (inclusive).
    """
    result = []
    for pol in pols:
        f = [compress_int(c, d) for c in pol.coef]
        result.append(Polynomial(f))
    return result

def decompress(pol: Polynomial, d: int) -> Polynomial:
    """
    Multiplies each coefficient of the given polynomial by `q/(2**d)`.
    Each coefficient of the given polynomial must be in range `0...2^d-1` (inclusive).
    """
    return Polynomial([decompress_int(c, d) for c in pol.coef])

def compress_int(x: int, d: int) -> int:
    assert d < ceil(log2(q))
    result = normal_round((2**d / q) * x) % (2**d)
    assert 0 <= result and result <= 2**d-1
    return result

def decompress_int(x: int, d: int) -> int:
    assert d < ceil(log2(q))
    if x < 0 or x > 2**d-1:
        raise ValueError()
    result = normal_round((q / 2**d) * x)
    return result
