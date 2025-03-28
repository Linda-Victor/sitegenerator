import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_leaf_node_to_html(self):
        node = LeafNode('p', 'Hello, world!')
        self.assertEqual(node.to_html(), '<p>Hello, world!</p>')
    def test_leaf_node_to_html2(self):
        node = LeafNode(None, 'DILMILSON')
        self.assertEqual(node.to_html(), 'DILMILSON')
    def test_leaf_node_to_html3(self):
        node = LeafNode ('c', None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_many_children(self):
        child_node1 = LeafNode('b', 'mamão')
        child_node2 = LeafNode(None, 'goiaba')
        child_node3 = LeafNode('d', 'tomate seco')
        parent_node = ParentNode('span', [child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), '<span><b>mamão</b>goiaba<d>tomate seco</d></span>')

    def test_to_html_error_no_tag(self):
        parent_node = ParentNode(None, 'Jacaré')
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()