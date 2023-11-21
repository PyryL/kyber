import unittest
from random import seed, randbytes
from kyber.utils.cbd import cbd

class TestCBD(unittest.TestCase):
    def setUp(self):
        seed(42)

    def test_cbd_returns_same_result_with_same_arguments(self):
        eta = 5
        argument = randbytes(320)   # 64*eta
        result1, result2 = cbd(argument, eta), cbd(argument, eta)
        self.assertEqual(result1, result2)

    def test_cbd_returns_different_results_with_different_arguments(self):
        eta = 5
        argument1 = randbytes(320)  # 64*eta
        argument2 = argument1[:-1] + bytes([argument1[-1] - 1])        # modify last byte
        result1, result2 = cbd(argument1, eta), cbd(argument2, eta)
        self.assertNotEqual(result1, result2)

    def test_cbd_throws_with_incorrect_argument_length(self):
        eta = 5
        argument = randbytes(321)
        with self.assertRaises(ValueError):
            cbd(argument, eta)

    def test_cbd_result_polynomial_degree(self):
        # test that CBD always outputs a polynomial with degree <= 255
        # also make sure that the degree is not always less than 255
        eta = 5
        some_had_degree_255 = False
        for _ in range(100):
            argument = randbytes(320)
            result = cbd(argument, eta)
            self.assertLessEqual(len(result.coefs), 256)
            if len(result.coefs) == 256:
                some_had_degree_255 = True
        self.assertTrue(some_had_degree_255)
