import unittest
from random import seed, randbytes
from kyber.ccakem import ccakem_generate_keys, ccakem_encrypt, ccakem_decrypt
from kyber.utils.pseudo_random import H
from kyber.constants import k, n, du, dv

class TestCCAKEM(unittest.TestCase):
    def test_ccakem_key_generation(self):
        private_key, public_key = ccakem_generate_keys()
        # check that keys have correct types and lengths
        self.assertEqual(type(private_key), bytes)
        self.assertEqual(type(public_key), bytes)
        self.assertEqual(len(private_key), 24 * k * n//8 + 96)
        self.assertEqual(len(public_key), 12 * k * n//8 + 32)
        # check that public key is concatenated inside private key
        private_key_section = private_key[12*k*n//8 : 24*k*n//8+32]
        self.assertEqual(private_key_section, public_key)

    def test_ccakem_encrypt(self):
        _, public_key = ccakem_generate_keys()
        ciphertext, shared_secret = ccakem_encrypt(public_key)
        self.assertEqual(type(ciphertext), bytes)
        self.assertEqual(type(shared_secret), bytes)
        self.assertEqual(len(ciphertext), du * k * n//8 + dv * n//8)
        self.assertEqual(len(shared_secret), 32)

    def test_ccakem_decrypt(self):
        # create seemingly valid private key by forming it from valid components
        seed(42)
        ciphertext = randbytes(du * k * n//8 + dv * n//8)
        public_key = randbytes(12 * k * n//8 + 32)
        private_key = randbytes(12*k*n//8) + public_key + H(public_key) + randbytes(32)
        shared_secret = ccakem_decrypt(ciphertext, private_key)
        self.assertEqual(type(shared_secret), bytes)
        self.assertEqual(len(shared_secret), 32)

    def test_ccakem_integration(self):
        private_key, public_key = ccakem_generate_keys()
        ciphertext, shared_secret1 = ccakem_encrypt(public_key)
        shared_secret2 = ccakem_decrypt(ciphertext, private_key)
        self.assertEqual(shared_secret1, shared_secret2)
