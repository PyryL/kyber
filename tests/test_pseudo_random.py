import unittest
from random import seed, randbytes
from kyber.utils.pseudo_random import prf, G, xof

class TestPseudoRandom(unittest.TestCase):
    def setUp(self):
        seed(42)

    def test_prf_result_length(self):
        # prf should return exactly 128 bytes
        result = prf(randbytes(17), randbytes(2))
        self.assertEqual(len(result), 128)

    def test_prf_returns_same_bytes_with_same_arguments(self):
        # two calls with same arguments should return same bytes
        argument1, argument2 = randbytes(17), randbytes(2)
        result1 = prf(argument1, argument2)
        result2 = prf(argument1, argument2)
        self.assertEqual(result1, result2)

    def test_prf_returns_different_results_with_different_arguments(self):
        result1 = prf(randbytes(17), randbytes(2))
        result2 = prf(randbytes(18), randbytes(2))
        self.assertNotEqual(result1, result2)


    def test_g_result_length(self):
        # G should return exactly 64 bytes
        result = G(randbytes(9))
        self.assertEqual(len(result), 64)

    def test_g_returns_same_bytes_with_same_arguments(self):
        # two calls with same arguments should return same bytes
        argument = randbytes(9)
        result1, result2 = G(argument), G(argument)
        self.assertEqual(result1, result2)

    def test_g_returns_different_results_with_different_arguments(self):
        argument1, argument2 = randbytes(9), randbytes(10)
        result1, result2 = G(argument1), G(argument2)
        self.assertNotEqual(result1, result2)


    def test_xof_returns_same_bytes_with_same_arguments(self):
        arguments = (randbytes(32), randbytes(1), randbytes(1))
        generator1 = xof(arguments[0], arguments[1], arguments[2])
        generator2 = xof(arguments[0], arguments[1], arguments[2])
        for i in range(1000):
            self.assertEqual(next(generator1), next(generator2), f"outputs differ at index {i}")

    def test_xof_returns_different_bytes_with_different_arguments(self):
        generator1 = xof(randbytes(32), randbytes(1), randbytes(1))
        generator2 = xof(randbytes(32), randbytes(1), randbytes(1))
        output1 = [next(generator1) for _ in range(1000)]
        output2 = [next(generator2) for _ in range(1000)]
        self.assertNotEqual(output1, output2)
