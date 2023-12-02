import unittest
from random import seed, randint
from numpy.polynomial.polynomial import Polynomial
import numpy as np
from kyber.entities.polring import PolynomialRing
from kyber.constants import q, n

# q = 3329

class TestPolynomialRing(unittest.TestCase):
    def test_initialization(self):
        pol = PolynomialRing([71, -5, 0, 1, 3329, 3330, 3328, 15])
        self.assertListEqual(pol.coefs, [71, 3324, 0, 1, 0, 1, 3328, 15])

    def test_initialization_with_no_limit_checks(self):
        pol = PolynomialRing([15, -3, 4012, -10514, 3329], check_limits=False)
        self.assertEqual(pol.coefs, [15, -3, 4012, -10514, 3329])

    def test_init_with_numpy_array(self):
        pol = PolynomialRing(np.array([-5, 123, 3330]))
        self.assertEqual(pol.coefs, [3324, 123, 1])
        self.assertEqual(type(pol.coefs), list)
        self.assertEqual(type(pol.coefs[0]), int)

    def test_init_with_random_inputs(self):
        # test with 1000 samples that randomily initialized polring matches expected
        seed(42)
        for _ in range(100):
            coef_count = randint(1, 500)
            coefs = [
                (1 if randint(1, 2) == 1 else -1) * randint(1, 10000)
                for _ in range(coef_count)
            ]
            pol = PolynomialRing(coefs)
            self.assertEqual(len(pol.coefs), min(coef_count, 256))
            expected_result = Polynomial(coefs) % Polynomial([1] + [0 for _ in range(n-1)] + [1])
            for i in range(len(pol.coefs)):
                self.assertEqual(pol.coefs[i], expected_result.coef[i] % q)

    def test_sum(self):
        pol1 = PolynomialRing([581,  -50,  100, 31, -4500, 4567, 11, 12])
        pol2 = PolynomialRing([1986, -150, -99, 34, 500,   0])
        # sum before mod [2567, -200, 1, 65, -4000, 4567, 11, 12]
        self.assertListEqual((pol1 + pol2).coefs, [2567, 3129, 1, 65, 2658, 1238, 11, 12])

    def test_multiplication(self):
        pol1 = PolynomialRing([15, -13, 0, 7,   472, -88,  112, 5])
        pol2 = PolynomialRing([2,  17,  8, 590, -11, -101, 91])
        # product before mod [30, 229, -101, 8760, -6772, 6532, 9312, 278430, -56838, 20053, 53558, -19375, 9687, 455]
        self.assertListEqual((pol1 * pol2).coefs, [30, 229, 3228, 2102, 3215, 3203, 2654, 2123, 3084, 79, 294, 599, 3029, 455])

    def test_multiplication_with_random_inputs(self):
        seed(42)
        for _ in range(100):
            pol1_degree, pol2_degree = randint(1, 500), randint(1, 500)
            coefs_1 = [randint(-4000, 4000) for _ in range(pol1_degree)]
            coefs_2 = [randint(-4000, 4000) for _ in range(pol2_degree)]
            result = PolynomialRing(coefs_1) * PolynomialRing(coefs_2)
            expected = (Polynomial(coefs_1) * Polynomial(coefs_2)) % Polynomial([1] + [0 for _ in range(n-1)] + [1])
            self.assertEqual(len(result.coefs), len(expected.coef))
            for i in range(len(result.coefs)):
                self.assertEqual(result.coefs[i], expected.coef[i] % q)

    def test_representation(self):
        pol = PolynomialRing([71, 3324, 0, 1, 0, 1, 3328, 15])
        self.assertEqual(pol.__repr__(), "PolRing(71, 3324, 0, 1, 0, 1, 3328, 15)")
