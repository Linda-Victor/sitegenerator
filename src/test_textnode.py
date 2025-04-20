import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_chico(self):
        chico = TextNode('É a que diz bad motherfucker', TextType.LINK, 'https://www.youtube.com/watch?v=NUuwd8Z0l_4')
        self.assertEqual(repr(chico), f'TextNode(É a que diz bad motherfucker, TextType.LINK, https://www.youtube.com/watch?v=NUuwd8Z0l_4)')

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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_text_not_in_enum(self):
        node = TextNode('ta errado', 'CARECA')
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()