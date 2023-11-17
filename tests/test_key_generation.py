import unittest
from kyber.encryption import generate_keys
from kyber.constants import k, n

class TestKeyGeneration(unittest.TestCase):
    def test_key_generation_output_characteristics(self):
        private_key, public_key = generate_keys()
        self.assertEqual(len(private_key), 12 * k * n//8)
        self.assertEqual(len(public_key), 12 * k * n//8 + 32)

    def test_key_generation_outputs_differ(self):
        # two subsequent calls should output completely different keypairs
        keypair1, keypair2 = generate_keys(), generate_keys()
        self.assertNotEqual(keypair1[0], keypair2[0])
        self.assertNotEqual(keypair1[1], keypair2[1])
