from textnode import TextType, TextNode

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
        
    