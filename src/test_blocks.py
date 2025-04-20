import unittest

from markdown_blocks import *

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        markdown = ''
        self.assertEqual(markdown_to_blocks(markdown), [])

    def test_markdown_to_blocks_many_lines(self):
        md = '\n\n\n\n\nababa\n\n\n\n\n\n'
        self.assertEqual(markdown_to_blocks(md), ['ababa'])

    def test_markdown_to_blocks_whitespace(self):
        md = ' \n\n \n\n\n  tortinho pra ESQUERDA \n\n\n CHEIA DE **GOMO**'
        self.assertEqual(markdown_to_blocks(md), ['tortinho pra ESQUERDA', 'CHEIA DE **GOMO**'])

    def test_block_to_block_type(self):
        self.assertEqual (block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
    def test_block_to_block_type_heading(self):
        self.assertEqual (block_to_block_type("# Heading 1"), BlockType.HEADING)
    def test_block_to_block_type_heading2(self):
        self.assertEqual (block_to_block_type("## Heading 2"), BlockType.HEADING)
    def test_block_to_block_type_code(self):
        self.assertEqual (block_to_block_type("```\ncode\n```"), BlockType.CODE)
    def test_block_to_block_type_quote(self):
        self.assertEqual (block_to_block_type("> This is a quote"), BlockType.QUOTE)
    def test_block_to_block_type_unord_list(self):
        self.assertEqual (block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)       
    def test_block_to_block_type_ord_list(self):
        self.assertEqual (block_to_block_type("1. Item 1\n2. Item 2"), BlockType.ORDERED_LIST)        
    def test_block_to_block_type_edge_case(self):
        self.assertEqual (block_to_block_type("#Not a heading"), BlockType.PARAGRAPH)


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
        
    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

