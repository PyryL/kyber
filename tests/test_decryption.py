import unittest
from random import seed, randbytes
from kyber.encryption import Decrypt
from kyber.constants import k, n, du, dv

class TestDecryption(unittest.TestCase):
    def setUp(self):
        seed(42)

    def test_decryption_outputs_valid_shared_secret(self):
        private_key = randbytes(32*12*k)
        ciphertext = randbytes(du*k*n//8 + dv*n//8)
        shared_secret = Decrypt(private_key, ciphertext).decrypt()
        self.assertEqual(type(shared_secret), bytes)
        self.assertEqual(len(shared_secret), 32)

    def test_decryption_raises_with_invalid_private_key(self):
        # this private key is one byte too long
        invalid_private_key = randbytes(32*12*k + 1)
        valid_ciphertext = randbytes(du*k*n//8 + dv*n//8)
        with self.assertRaises(ValueError):
            Decrypt(invalid_private_key, valid_ciphertext)

    def test_decryption_raises_with_invalid_ciphertext(self):
        # this ciphertext is one byte too short
        valid_private_key = randbytes(32*12*k)
        invalid_ciphertext = randbytes(du*k*n//8 + dv*n//8 - 1)
        with self.assertRaises(ValueError):
            Decrypt(valid_private_key, invalid_ciphertext)
