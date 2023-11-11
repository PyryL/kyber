import unittest
from kyber.keygen import generate_keys
from kyber.encrypt import Encrypt
from kyber.decrypt import Decrypt

class TestIntegration(unittest.TestCase):
    def test_encryption_symmetry(self):
        # test the whole process of key generation, encryption and decryption
        private_key, public_key = generate_keys()
        encrypter = Encrypt(public_key)
        ciphertext = encrypter.encrypt()
        decrypted_shared_secret = Decrypt(private_key, ciphertext).decrypt()
        self.assertEqual(encrypter.secret, decrypted_shared_secret)
        self.assertEqual(len(encrypter.secret), 32)