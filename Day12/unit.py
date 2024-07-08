import unittest
from main import calcGroups

class TestExample(unittest.TestCase):
    def test_calcGroups(self):
        res = calcGroups('.##.##')
        self.assertEqual(res, [2,2])


if __name__ == '__main__':
    unittest.main()