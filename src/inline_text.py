import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.extend([node])
            continue
        text = node.text
        first_delim = text.find(delimiter)
        second_delim = text[first_delim + len(delimiter):].find(delimiter)

        if first_delim == -1:
            new_nodes.extend([node])
            continue
        
        if first_delim != -1 and second_delim == -1:
            raise Exception("Invalid Markdown syntax")
        
        if second_delim != -1:
            second_delim = second_delim + len(delimiter) + first_delim
            split_text = text[:second_delim].split(delimiter)

            if split_text[0] != "":
                normal_text = TextNode(split_text[0], TextType.NORMAL)
                new_nodes.extend([normal_text])

            delimited_text = TextNode(split_text[1], text_type)
            new_nodes.extend([delimited_text])

            if len(text[second_delim + len(delimiter):]) > 0:
                remainder_text = text[second_delim + len(delimiter):]
                remainder_node = TextNode(remainder_text, TextType.NORMAL)
                remainder_nodes =  split_nodes_delimiter([remainder_node], delimiter, text_type)
                new_nodes.extend(remainder_nodes)
                continue

    return new_nodes

def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text):
    regex=r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches
