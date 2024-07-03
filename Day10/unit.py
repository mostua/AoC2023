import unittest
from main import convertToNet, Input, Dfs

class TestConvert(unittest.TestCase):
    def test_onePoint(self):
        rows = ['...', '.S.', '...']
        input = Input(rows)
        net = convertToNet(input)
        self.assertEqual(net.maxX, 2)
        self.assertEqual(net.maxY, 2)



class TestDfs(unittest.TestCase):
    def test_simplLoop(self):
        rows = ['S7', 'LJ']
        input = Input(rows)
        # step 1
        net = convertToNet(input)
        self.assertEqual(net.maxX, 1)
        self.assertEqual(net.maxY, 1)
        # step 2
        dfs = Dfs(net)
        dfs.execute()
        loop = dfs.findLoop()
        print(loop)
        self.assertEqual(len(loop), 4)
        


if __name__ == '__main__':
    unittest.main()