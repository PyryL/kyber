import unittest
import pytest
from kyber.utils.byte_conversion import bits_to_bytes, bytes_to_bits

class TestByteConversion(unittest.TestCase):
    def test_bits_to_bytes(self):
        bits = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0]
        expected_bytes = bytes([149, 68])
        self.assertEqual(bits_to_bytes(bits), expected_bytes)

    def test_bits_to_bytes_invalid_bit_value(self):
        # integer 2 is not a valid bit
        bits = [1, 0, 0, 1, 0, 1, 2, 1, 0, 1, 0, 0, 0, 1, 0, 0]
        with pytest.raises(ValueError):
            bits_to_bytes(bits)

    def test_bits_to_bytes_invalid_input_length(self):
        # input length should be multipla of 8
        bits = [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0]
        with pytest.raises(ValueError):
            bits_to_bytes(bits)

    def test_bytes_to_bits(self):
        input_bytes = bytes([149, 68])
        expected_bits = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0]
        self.assertEqual(bytes_to_bits(input_bytes), expected_bits)
