from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delimiters = ['**', '_', '`']

    if delimiter not in delimiters:
        raise Exception(f'invalid Markdown syntax: {delimiter}')
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        result = []

        while delimiter in text:
            start_index = text.find(delimiter)
            if start_index > 0:
                result.append(TextNode(text[:start_index], TextType.TEXT))

            end_index = text.find(delimiter, start_index + len(delimiter))
            if end_index == -1:
                raise Exception(f'No closing delimiter {delimiter} found')
            
            content = text[start_index + len(delimiter):end_index]
            result.append(TextNode(content, text_type)) 
            text = text[end_index + len(delimiter):]
        
        if text:
            result.append(TextNode(text, TextType.TEXT))

        new_nodes.extend(result)

    return new_nodes   
        
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        imagetext_and_imageurl = extract_markdown_images(node.text)
        if imagetext_and_imageurl == [] and node.text != '':
            new_nodes.append(node)
        sections = []
        for i, image_and_url in enumerate(imagetext_and_imageurl):
            if sections == []:   
                this_section = node.text.split(f'![{image_and_url[0]}]({image_and_url[1]})', 1)
            else:
                this_section = sections[0].split(f'![{image_and_url[0]}]({image_and_url[1]})', 1)
                del sections[0]
            if len(this_section) != 2:
                raise Exception('invalid markdown, image selection not closed')
            if this_section[0] != '':
                new_nodes.append(TextNode(this_section[0], TextType.TEXT))
            new_nodes.append(TextNode(image_and_url[0], TextType.IMAGE, image_and_url[1]))
            if i == len(imagetext_and_imageurl) - 1:
                if this_section[1] != '':
                    new_nodes.append(TextNode(this_section[1], TextType.TEXT))
            else:
                sections.append(this_section[1])
    return new_nodes
        
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        linktext_and_linkurl = extract_markdown_links(node.text)
        if linktext_and_linkurl == [] and node.text != '':
            new_nodes.append(node)
        sections = []
        for i, text_and_url in enumerate(linktext_and_linkurl):
            if sections == []:   
                this_section = node.text.split(f'[{text_and_url[0]}]({text_and_url[1]})', 1)
            else:
                this_section = sections[0].split(f'[{text_and_url[0]}]({text_and_url[1]})', 1)
                del sections[0]
            if len(this_section) != 2:
                raise Exception('invalid markdown, image selection not closed')
            if this_section[0] != '':
                new_nodes.append(TextNode(this_section[0], TextType.TEXT))
            new_nodes.append(TextNode(text_and_url[0], TextType.LINK, text_and_url[1]))
            if i == len(linktext_and_linkurl) - 1:
                if this_section[1] != '':
                    new_nodes.append(TextNode(this_section[1], TextType.TEXT))
            else:
                sections.append(this_section[1])
    return new_nodes

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    first_delimiters = split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(node, "**", TextType.BOLD), "_", TextType.ITALIC), "`", TextType.CODE)
    new_nodes = split_nodes_link(split_nodes_image(first_delimiters))
    return new_nodes


def extract_markdown_images(text):
    text_and_url = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return text_and_url
    
def extract_markdown_links(text):
    text_and_link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return text_and_link
