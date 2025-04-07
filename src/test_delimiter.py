import unittest

from delimiter import *
from textnode import TextNode, TextType

class TestDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        nodes = [
            TextNode('TOMA NO CU O FLAMENGO', TextType.BOLD), 
            TextNode('Aqui é **TORCIDA JOVEM VASCO** CARALHO', TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, '**', TextType.BOLD), 
            [
                TextNode('TOMA NO CU O FLAMENGO', TextType.BOLD),
                TextNode('Aqui é ', TextType.TEXT),
                TextNode('TORCIDA JOVEM VASCO', TextType.BOLD),
                TextNode(' CARALHO', TextType.TEXT)
            ]
        )
    def test_split_nodes_delimiter_error(self):
        nodes = [
            TextNode('**DELIMITOU ERRADO', TextType.TEXT)
        ]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, '**', TextType.TEXT)
    def test_split_nodes_delimiter_code(self):
        nodes = [
            TextNode('def a_brabona_msm', TextType.CODE),
            TextNode('aí tu bota `while fumar(a_brabona_msm)`', TextType.TEXT),
            TextNode('finaliza com `return disney_hong_kong` e fechou', TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, '`', TextType.CODE),
            [
                TextNode('def a_brabona_msm', TextType.CODE),
                TextNode('aí tu bota ', TextType.TEXT),
                TextNode('while fumar(a_brabona_msm)', TextType.CODE),
                TextNode('finaliza com ', TextType.TEXT),
                TextNode('return disney_hong_kong', TextType.CODE),
                TextNode(' e fechou', TextType.TEXT)
            ]
        )

class TestExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    def test_extract_markdown_links_empty(self):
        text = "tá vazio"
        self.assertEqual(extract_markdown_links(text), [])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links2(self):
        self.maxDiff = None
        node = [
            TextNode('top 5 mais brabas do jethro tull:[reasons for waiting, ](https://www.youtube.com/watch?v=iybAyDFrhhI)[cross-eyed mary, ](https://www.youtube.com/watch?v=0ufuH4vZ77w)[skating away on the thin ice of a new day, ](https://www.youtube.com/watch?v=S5D9HZyYI6g)[with you there to help me, ](https://www.youtube.com/watch?v=gfKzPV-Ely4)e a mais brabona de todas: [thick as a brick.](https://www.youtube.com/watch?v=X15PsqN0DHc)', TextType.TEXT)
            ]
        
        self.assertEqual(split_nodes_link(node),
            [
                TextNode('top 5 mais brabas do jethro tull:', TextType.TEXT),
                TextNode('reasons for waiting, ', TextType.LINK, 'https://www.youtube.com/watch?v=iybAyDFrhhI'),
                TextNode('cross-eyed mary, ', TextType.LINK, 'https://www.youtube.com/watch?v=0ufuH4vZ77w'),
                TextNode('skating away on the thin ice of a new day, ', TextType.LINK, 'https://www.youtube.com/watch?v=S5D9HZyYI6g'),
                TextNode('with you there to help me, ', TextType.LINK, 'https://www.youtube.com/watch?v=gfKzPV-Ely4'),
                TextNode('e a mais brabona de todas: ', TextType.TEXT),
                TextNode('thick as a brick.', TextType.LINK, 'https://www.youtube.com/watch?v=X15PsqN0DHc')
            ])

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT)
        self.assertEqual(split_nodes_link([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ]
        )

    def test_split_image_exception(self):
        node = TextNode(
            'this is text with [wrong image markdown',
            TextType.TEXT
        )
        with self.assertRaises(Exception):
            split_nodes_image(node)

    def test_split_link_exception(self):
        node = TextNode(
            'this is text with [wrong image markdown',
            TextType.TEXT
        )
        with self.assertRaises(Exception):
            split_nodes_link(node)

    def test_text_to_textnodes(self):
        self.maxDiff = None
        node = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'

        self.assertEqual(text_to_textnodes(node),
                [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
            )

if __name__ == "__main__":
    unittest.main()