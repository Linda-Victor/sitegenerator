import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode('This is one', TextType.ITALIC)
        node2 = TextNode('This is two', TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_eq3(self):
        node = TextNode("They're taking the hobbits to isengard", TextType.BOLD)
        node2 = TextNode("They're taking the hobbits to insergrad", TextType.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()