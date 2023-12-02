import unittest
from random import seed, randint
from kyber.utils.compression import compress, decompress
from kyber.entities.polring import PolynomialRing

class TestCompression(unittest.TestCase):
    def test_compression_symmetry(self):
        # test that polynomial ring does not change when it is compressed and decompressed
        seed(42)
        for _ in range(100):
            polynomial = PolynomialRing([randint(0, 2047) for _ in range(256)])
            decompressed = decompress(polynomial, 11)
            compressed = compress([decompressed], 11)[0]
            self.assertListEqual(list(polynomial.coefs), list(compressed.coefs))

    def test_compression(self):
        polynomial = PolynomialRing([416, 2913, 0, 1248])
        expected_result = PolynomialRing([1, 7, 0, 3])
        self.assertEqual(compress([polynomial], 3)[0], expected_result)

    def test_compression_result_coefficients_in_range(self):
        # each coefficient in the result should be in range 0...2**d-1 (inclusive)
        d = 11
        polynomial = PolynomialRing([4000, -700, 0, 32])
        result = compress([polynomial], d)[0]
        for c in result.coefs:
            self.assertTrue(0 <= c and c <= 2**d-1)


    def test_decompression(self):
        polynomial = PolynomialRing([1, 7, 0, 3])
        expected_result = PolynomialRing([416, 2913, 0, 1248])
        self.assertEqual(decompress(polynomial, 3), expected_result)

    def test_decompression_raises_with_negative_coefficient(self):
        # coefficient should not be negative
        polynomial = PolynomialRing([2, -1, 3])
        with self.assertRaises(ValueError):
            decompress(polynomial, 3)

    def test_decompression_raises_with_too_large_coefficient(self):
        # coefficient should not be greather than 2**d-1 = 7
        polynomial = PolynomialRing([2, 8, 3])
        with self.assertRaises(ValueError):
            decompress(polynomial, 3)# 
