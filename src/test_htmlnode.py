import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("PEGA NO BREU JOGA LÁ", "Agropesca Jacaré", None, {"href": "https://www.youtube.com/watch?v=TFdO7oqkMzI"})
        self.assertEqual(node.props_to_html(), ' href="https://www.youtube.com/watch?v=TFdO7oqkMzI"')
    def test_props_to_html2(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual(node.props_to_html(), '')
    def test_props_to_html3(self):
        node = HTMLNode('tornado', "de cartas", ['no', 'castelo'], {'5': '2+2', '94': '587 + 932'})
        self.assertEqual(node.props_to_html(), ' 5="2+2" 94="587 + 932"')

if __name__ == "__main__":
    unittest.main()