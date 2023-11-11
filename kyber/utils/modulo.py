import numpy as np
from numpy.polynomial.polynomial import Polynomial
from kyber.constants import n, q

def matmod(
        matrix: np.ndarray,
        pol_divisor: Polynomial = None,
        int_divisor: int = None
    ) -> np.ndarray:
    """
    Applies `polmod` to each element of the given matrix of polynomials.
    :param matrix A matrix of polynomials
    :param pol_divisor A polynomial divisor. Only for testing purposes. (default: x^n+1)
    :param int_divisor An integer divisor. Only for testing purposes. (default: constant q)
    :returns A new matrix of polynomials.
    """

    result = matrix.copy()
    for index, item in np.ndenumerate(matrix):
        result[index] = polmod(item, pol_divisor, int_divisor)
    return result

def polmod(pol: Polynomial, pol_divisor: Polynomial = None, int_divisor: int = None) -> Polynomial:
    """
    Finds given polynomial modulo another polynomial and coefficients modulo an integer.
    :param pol The polynomial to be modded
    :param pol_divisor A polynomial divisor. Only for testing purposes. (default: x^n+1)
    :param int_divisor An integer divisor. Only for testing purposes. (default: constant q)
    :returns The remainder of polynomial division whose coefficients are taken modulo int_divisor.
    """

    # divide the given polynomial by another polynomial and take the remainder
    if pol_divisor is not None:
        divisor = pol_divisor
    else:
        divisor = Polynomial([1] + [0 for _ in range(n-1)] + [1])       # x^n + 1
    pol = pol % divisor

    # divide each coefficient of the polynomial by an integer and take the remainder
    divisor = int_divisor if int_divisor is not None else q
    for i in range(len(pol.coef)):
        pol.coef[i] %= divisor

    return pol
