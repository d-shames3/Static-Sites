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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text

        if text == "":
            continue

        matches = extract_markdown_images(text)
        
        if not matches:
            new_nodes.extend([node])
            continue

        match = matches[0]
        image_alt, image_link = match[0], match[1] 
        sections = text.split(f"![{image_alt}]({image_link})", 1)
        
        if sections[0] != "":
            normal_text = TextNode(sections[0], TextType.NORMAL)
            new_nodes.extend([normal_text])
        
        image_node = TextNode(match[0], TextType.IMAGE, match[1])
        new_nodes.extend([image_node])

        if len(sections) > 1:
            remainder_node = TextNode(sections[1], TextType.NORMAL)
            remainder_nodes = split_nodes_image([remainder_node])
            new_nodes.extend(remainder_nodes)
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text

        if text == "":
            continue

        matches = extract_markdown_links(text)
        
        if not matches:
            new_nodes.extend([node])
            continue

        match = matches[0]
        image_alt, image_link = match[0], match[1] 
        sections = text.split(f"[{image_alt}]({image_link})", 1)
        
        if sections[0] != "":
            normal_text = TextNode(sections[0], TextType.NORMAL)
            new_nodes.extend([normal_text])
        
        image_node = TextNode(match[0], TextType.LINK, match[1])
        new_nodes.extend([image_node])

        if len(sections) > 1:
            remainder_node = TextNode(sections[1], TextType.NORMAL)
            remainder_nodes = split_nodes_link([remainder_node])
            new_nodes.extend(remainder_nodes)

    return new_nodes
