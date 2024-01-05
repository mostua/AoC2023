import unittest
from main import Play, Value

class TestGetValue(unittest.TestCase):

    def test_TWO_PAIR(self):
        play = Play("AAKK1", 0)
        self.assertEqual(play.getValue(), Value.TWO_PAIR)

    def test_HIGH_CARD(self):
        play = Play("12345", 0)
        self.assertEqual(play.getValue(), Value.HIGH_CARD)

class TestSorting(unittest.TestCase):

    def test_diffrent_rank(self):
        play1 = Play("AAAA1", 3)
        play2 = Play("AAAK1", 2)
        play3 = Play("AAKK1", 1)
        res = sorted([play1, play2, play3])
        self.assertEqual(res[0].bid, 1)
        self.assertEqual(res[1].bid, 2)
        self.assertEqual(res[2].bid, 3)

    def test_same_rank(self):
        play1 = Play("KK677", 2)
        play2 = Play("KTJJT", 1)
        res = sorted([play1, play2])
        self.assertEqual(res[0].bid, 1)
        self.assertEqual(res[1].bid, 2)




if __name__ == '__main__':
    unittest.main()