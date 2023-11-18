import unittest
from numpy.polynomial.polynomial import Polynomial
from random import seed, randbytes, randint
from kyber.utils.encoding import encode, decode

class TestEncoding(unittest.TestCase):
    def setUp(self):
        seed(42)
        self.l = 5
        self.data = randbytes(32 * self.l)
        self.polynomial = Polynomial([randint(0, 1) for _ in range(256)])
        self.polynomial2 = Polynomial([randint(0, 1) for _ in range(256)])

    def test_encoding_symmetry(self):
        polynomials = decode(self.data, self.l)
        restored_data = encode(polynomials, self.l)
        self.assertEqual(self.data, restored_data)

    def test_decode_coefficients(self):
        polynomial = decode(self.data, self.l)[0]
        for c in polynomial.coef:
            self.assertTrue(0 <= int(c) or int(c) <= 2**self.l-1)

    def test_decode_degree(self):
        polynomial = decode(self.data, self.l)[0]
        self.assertEqual(len(polynomial.coef), 256)

    def test_decode_raises_with_invalid_argument_length(self):
        data = self.data + bytes([42])
        with self.assertRaises(ValueError):
            decode(data, self.l)

    def test_encode_length_with_single_polynomial(self):
        result = encode([self.polynomial], self.l)
        self.assertEqual(len(result), 32*self.l)

    def test_encode_length_with_multiple_polynomials(self):
        result = encode([self.polynomial, self.polynomial2], self.l)
        self.assertEqual(len(result), 2*32*self.l)

    def test_encode_raises_with_too_large_coefficient(self):
        # each coefficient should be in range 0...2**l-1 (inclusive)
        coefs = [i % (2**self.l-1) for i in range(1, 257)]
        coefs[4] = 2**self.l
        polynomial = Polynomial(coefs)
        with self.assertRaises(ValueError):
            encode([polynomial], self.l)

    def test_encode_raises_with_too_high_degree(self):
        # encode should be given a polynomial with degree of 255, not 256
        coefs = [1 for _ in range(257)]
        polynomial = Polynomial(coefs)
        with self.assertRaises(ValueError):
            encode([polynomial], self.l)
