import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq1(self):
        node1 = LeafNode("a", "An a tag", {"href": "https://www.google.com", "target": "_blank"})
        node2 = LeafNode("a", "An a tag", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node1.to_html(), node2.to_html())

    def test_eq2(self):
        node1 = LeafNode("a", "An a tag", {"href": "https://www.google.com", "target": "_blank"})
        node2 = LeafNode("a", "An a tag", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node1.__repr__(), node2.__repr__())


if __name__ == "__main__":
    unittest.main()