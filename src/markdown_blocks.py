from enum import Enum

from htmlnode import ParentNode
from delimiter import text_to_textnodes
from textnode import TextNode, text_node_to_html_node, TextType

BlockType = Enum('BlockType', ['PARAGRAPH', 'HEADING', 'CODE', 'QUOTE', 'UNORDERED_LIST', 'ORDERED_LIST'])

def block_to_block_type(markdown):
    
    def check_beginning_lines(lines, character):
        for line in lines:
            if line.startswith(character) == False:
                return False
        return True
    
    def is_ordered_list(lines):
        expected_number = 1
        for line in lines:
            if not line.startswith(f"{expected_number}. "):
                return False
            expected_number += 1
        return True

    markdown_lines = markdown.split('\n')

    if (markdown[:2] == "# " or
        markdown[:3] == '## ' or
        markdown[:4] == '### ' or
        markdown[:5] == '#### ' or
        markdown[:6] == '##### ' or
        markdown[:7] == '###### '):
        return BlockType.HEADING
    if markdown[:3] == markdown[-3:] == '```':
        return BlockType.CODE
    if check_beginning_lines(markdown_lines, '>'):
        return BlockType.QUOTE
    if check_beginning_lines(markdown_lines, '- '):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(markdown_lines):
        return BlockType.ORDERED_LIST 
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    new_blocks = []
    for block in blocks:
        new_block = block.strip()
        if new_block == '':
            continue
        new_blocks.append(new_block)
    return new_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children_nodes.append(html_node)
    return ParentNode('div', children_nodes, None)
        
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError('invalid block type')

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split('\n')
    paragraph = ' '.join(lines)
    children = text_to_children(paragraph)
    return ParentNode('p', children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f'invalid heading level: {level}')
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f'h{level}', children)

def code_to_html_node(block):
    if not block.startswith('```') or not block.endswith('```'):
        raise ValueError('invalid code block')
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode('code', [child])
    return ParentNode('pre', [code])

def olist_to_html_node(block):
    items = block.split('\n')
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode('li', children))
    return ParentNode('ol', html_items)

def ulist_to_html_node(block):
    items = block.split('\n')
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode('li', children))
    return ParentNode('ul', html_items)

def quote_to_html_node(block):
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        if not line.startswith('>'):
            raise ValueError('invalid quote block')
        new_lines.append(line.lstrip('>').strip())
    content = ' '.join(new_lines)
    children = text_to_children(content)
    return ParentNode('blockquote', children)
