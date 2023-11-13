import unittest
from random import seed, randbytes
from kyber.encrypt import Encrypt
from kyber.constants import k, n

class TestEncryption(unittest.TestCase):
    def test_encryption_raises_with_invalid_input(self):
        # this public key is one byte too short
        seed(42)
        invalid_public_key = randbytes(12 * k * n//8 + 31)
        with self.assertRaises(ValueError):
            Encrypt(invalid_public_key)

    def test_encryption_generates_valid_shared_secret(self):
        seed(42)
        encrypter = Encrypt(randbytes(12 * k * n//8 + 32))
        self.assertEqual(len(encrypter.secret), 32)
