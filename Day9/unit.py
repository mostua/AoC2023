import unittest

class TestExample(unittest.TestCase):
    def test_OK(self):
        self.assertEqual('OK', 'OK')


if __name__ == '__main__':
    unittest.main()