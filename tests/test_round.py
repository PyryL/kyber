import unittest
from kyber.utils.round import normal_round

class TestRound(unittest.TestCase):
    def test_normal_round(self):
        self.assertEqual(normal_round(5.5), 6)
        self.assertEqual(normal_round(7.9), 8)
        self.assertEqual(normal_round(1.234), 1)
        self.assertEqual(normal_round(-3.5), -3)
        self.assertEqual(normal_round(-3.6), -4)
        self.assertEqual(normal_round(-3.2), -3)
        self.assertEqual(normal_round(-0.2), 0)
        self.assertEqual(normal_round(0), 0)
        self.assertEqual(normal_round(0.18), 0)
