import unittest
from main import parseNode, Node

class TestParseNet(unittest.TestCase):

    def test_TWO_PAIR(self):
        net = parseNode('AAA = (BBB, CCC)')
        self.assertEqual(net, Node(id = 'AAA', left='BBB', right='CCC'))




if __name__ == '__main__':
    unittest.main()