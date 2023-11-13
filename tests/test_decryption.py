import unittest
from random import seed, randbytes
from kyber.decrypt import Decrypt
from kyber.constants import k

class TestDecryption(unittest.TestCase):
    def test_decryption_raises_with_invalid_input(self):
        # this private key is one byte too long
        seed(42)
        invalid_private_key = randbytes(32*12*k + 1)
        ciphertext_placeholder = ()
        with self.assertRaises(ValueError):
            Decrypt(invalid_private_key, ciphertext_placeholder)
