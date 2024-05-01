import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_eq1(self):
        node1 = ParentNode("p", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ], None)
        
        self.assertEqual(node1.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    


if __name__ == "__main__":
    unittest.main()