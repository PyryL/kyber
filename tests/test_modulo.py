import unittest
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from kyber.utils.modulo import matmod, polmod

class TestModulo(unittest.TestCase):
    def setUp(self):
        self.polynomial = Polynomial([72, -2, 0, 52, -3, 17])
        self.pol_divisor = Polynomial([1, 0, 0, 1])
        self.int_divisor = 7

    def test_polmod(self):
        # remainder of division polynomial/pol_divisor is -17x^2+x+20
        # then each coefficient is taken modulo int_divisor to get the expected_result
        result = polmod(self.polynomial, self.pol_divisor, self.int_divisor)
        expected_result = Polynomial([6, 1, 4])
        self.assertEqual(result, expected_result)

    def test_matmod(self):
        # basically the same test than `test_polmod` but for a matrix of two identical polynomials
        matrix = np.array([self.polynomial, self.polynomial])
        expected_result = Polynomial([6, 1, 4])
        result = matmod(matrix, self.pol_divisor, self.int_divisor)
        self.assertEqual(result.shape, (2, ))
        self.assertEqual(result[0], expected_result)
        self.assertEqual(result[1], expected_result)
