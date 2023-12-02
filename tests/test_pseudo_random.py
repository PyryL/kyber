import unittest
from random import seed, randbytes, randint
from kyber.utils.pseudo_random import prf, G, xof, kdf, H

class TestPseudoRandom(unittest.TestCase):
    def setUp(self):
        seed(42)

    def test_prf_case_output(self):
        # test case calculated with another tool found online
        expected_output = "e19287039a95cebe6fb2994fef8b2773988c73781729ad420bbaa9d0988d58e19fe82b49e6c68ea589a92c81463c8cf2513710ac80beba2eeac4c5008742d60d3b0ee8e7fd5b404fa126791f8cd1a6c6822fcb14523db0e591eded03b259182ab4330f0712e776aab5da9168e39cae9743b418cf27f5c817329f5a0f2b093624"
        self.assertEqual(prf(bytes.fromhex("c0ffee"), bytes.fromhex("c0de")), bytes.fromhex(expected_output))

    def test_prf_result_length(self):
        # prf should return exactly 128 bytes
        result = prf(randbytes(17), randbytes(2))
        self.assertEqual(len(result), 128)

    def test_prf_returns_same_bytes_with_same_arguments(self):
        # two calls with same arguments should return same bytes
        argument1, argument2 = randbytes(17), randbytes(2)
        result1 = prf(argument1, argument2)
        result2 = prf(argument1, argument2)
        self.assertEqual(result1, result2)

    def test_prf_returns_different_results_with_different_arguments(self):
        result1 = prf(randbytes(17), randbytes(2))
        result2 = prf(randbytes(18), randbytes(2))
        self.assertNotEqual(result1, result2)


    def test_kdf_sample_output(self):
        payload = bytes.fromhex("9d79b1a37f31801cd11a6706fb40d6bd57526846903bb13ede562439e9c1b823a96089bca71f3d1a6d2d3cadb3669cbd50e165e434249d8b829f411669842a979911036cf3e822086ecaa0075a69fc178ba8f83718aa8f3bd1f65e8144e61d9ab30fcb06a6c1ad8f2906e732b10f4db789d35ea68c088ab3f648818b")
        result = kdf(payload, 93)
        expected_result = bytes.fromhex("8d85b491f075655ec2620be0ed8a061fe481c989ca609987ad1aeec1ddbc66c9affbacb27d7c163f4c709de77e470607d63315089e0d69c93351f650417e612f7b6a63885f0a1e91836d15bbb23d76b84e85da0c54090d493202abc85f")
        self.assertEqual(result, expected_result)

    def test_kdf_random_inputs(self):
        outputs = set()
        for _ in range(100):
            output_length = randint(1, 2000)
            output = kdf(randbytes(randint(1, 2000)), output_length)
            self.assertEqual(len(output), output_length)
            self.assertFalse(output in outputs)
            outputs.add(output)

    def test_kdf_case_output(self):
        expected_result = bytes.fromhex("f17e4c7f0ac30b7cb7b26791e2d3151d59bbcbb4c83357b2bb07f0043bf2d96a00b37b79b5f3153aba5d")
        self.assertEqual(kdf(bytes.fromhex("c0ffee"), 42), expected_result)


    def test_g_result_length(self):
        # G should return exactly 64 bytes
        result = G(randbytes(9))
        self.assertEqual(len(result), 64)

    def test_g_returns_same_bytes_with_same_arguments(self):
        # two calls with same arguments should return same bytes
        argument = randbytes(9)
        result1, result2 = G(argument), G(argument)
        self.assertEqual(result1, result2)

    def test_g_returns_different_results_with_different_arguments(self):
        argument1, argument2 = randbytes(9), randbytes(10)
        result1, result2 = G(argument1), G(argument2)
        self.assertNotEqual(result1, result2)

    def test_g_case_output(self):
        expected_result = "16e16e7ebc463111d9f0dddccfa9d33152706bcdf41bf2c89d928f4b4463e4576237b569a71fdb7f168f4932c43430624a80e135eb8b6a1aefc7dbd1210d97e5"
        self.assertEqual(G(bytes.fromhex("c0ffee")), bytes.fromhex(expected_result))


    def test_xof_returns_same_bytes_with_same_arguments(self):
        arguments = (randbytes(32), randbytes(1), randbytes(1))
        generator1 = xof(arguments[0], arguments[1], arguments[2])
        generator2 = xof(arguments[0], arguments[1], arguments[2])
        for i in range(1000):
            self.assertEqual(next(generator1), next(generator2), f"outputs differ at index {i}")

    def test_xof_returns_different_bytes_with_different_arguments(self):
        generator1 = xof(randbytes(32), randbytes(1), randbytes(1))
        generator2 = xof(randbytes(32), randbytes(1), randbytes(1))
        output1 = [next(generator1) for _ in range(1000)]
        output2 = [next(generator2) for _ in range(1000)]
        self.assertNotEqual(output1, output2)

    def test_xof_case_output(self):
        generator = xof(bytes.fromhex("c0ffee"), bytes.fromhex("c0de"), bytes.fromhex("0ff1ce"))
        output = bytearray()
        for _ in range(30):
            output += next(generator)
        expected_output = bytes.fromhex("74349c255f965bc5c45c0a570a35cdbd9d32899abcf62fd8f68a35df8446")
        self.assertEqual(output, expected_output)


    def test_h_sample_output(self):
        payload = bytes.fromhex("9d79b1a37f31801cd11a6706fb40d6bd57526846903bb13ede562439e9c1b823a96089bca71f3d1a6d2d3cadb3669cbd50e165e434249d8b")
        expected_output = bytes.fromhex("377d53fb7115593aa9e317b2aa2251d9edcad8388986152638bab0d4af1e4443")
        self.assertEqual(H(payload), expected_output)

    def test_h_random_inputs(self):
        outputs = set()
        for _ in range(100):
            output = H(randbytes(randint(1, 2000)))
            self.assertEqual(len(output), 32)
            self.assertFalse(output in outputs)
            outputs.add(output)

    def test_h_case_output(self):
        expected_output = bytes.fromhex("47b147ef11cd3eb6c9bf988470a83a21e2a5c39782dd25d1483b4a8d129ad291")
        self.assertEqual(H(bytes.fromhex("c0ffee")), expected_output)
