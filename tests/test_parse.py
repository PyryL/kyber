import unittest
from kyber.utils.parse import parse
from typing import Generator

def sample_generator(seed: int = 0) -> Generator[bytes, None, None]:
    """A generator that yields one byte at a time `seed, seed+1, ..., 255, 0, 1, ...`."""
    i = seed
    while True:
        yield bytes([i % 256])
        i += 1

class TestParse(unittest.TestCase):
    def test_parse_outputted_polynomial_characteristics(self):
        pol = parse(sample_generator())
        self.assertEqual(len(pol.coef), 256)
        for c in pol.coef:
            self.assertTrue(0 <= c and c <= 4095)

    def test_parse_outputs_same_polynomial_with_same_input(self):
        polynomial1 = parse(sample_generator())
        polynomial2 = parse(sample_generator())
        self.assertEqual(polynomial1, polynomial2)

    def test_parse_outputs_different_polynomials_with_different_inputs(self):
        polynomial1 = parse(sample_generator())
        polynomial2 = parse(sample_generator(42))
        self.assertNotEqual(polynomial1, polynomial2)
