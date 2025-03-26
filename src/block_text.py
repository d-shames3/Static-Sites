from htmlnode import ParentNode
from textnode import text_node_to_html_node
from inline_text import text_to_textnodes
import re


def split_block(text):
    split_newline = text.split("\n\n")
    whitespace_stripped = list(map(lambda string: string.strip(), split_newline))

    return whitespace_stripped


def block_to_block_type(markdown_block):
    split_block_lines = markdown_block.split("\n")
    n_rows = len(split_block_lines) + 1
    if "# " in markdown_block[:7]:
        return "heading"
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return "code"
    elif all(line.startswith(">") for line in split_block_lines):
        return "quote"
    elif all(
        (line.startswith("* ") or line.startswith("- ")) for line in split_block_lines
    ):
        return "unordered_list"
    elif [line[:3] for line in split_block_lines] == [
        f"{i}. " for i in range(1, n_rows)
    ]:
        return "ordered_list"
    else:
        return "paragraph"


def get_html_tag(block_type):
    block_type_to_html_tag = {
        "paragraph": "p",
        "quote": "blockquote",
        "unordered_list": "ul",
        "ordered_list": "ol",
        "code": "code",
        "heading": "h",
    }
    return block_type_to_html_tag[block_type]


def text_to_children(markdown_block):
    text_nodes = text_to_textnodes(markdown_block)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return html_nodes


def markdown_to_html_node(markdown_string):
    parent = ParentNode("div", children=[])

    block_list = split_block(markdown_string)
    for block in block_list:
        type = block_to_block_type(block)
        tag = get_html_tag(type)

        if type == "heading":
            heading_number = len(block.split(" ", 1)[0])
            tag += str(heading_number)
            heading_node = ParentNode(tag, children=[])
            delimiter = r"\#{1,6} "
            clean_block = re.sub(delimiter, "", block)
            children = text_to_children(clean_block)
            heading_node.children.extend(children)
            parent.children.append(heading_node)

        elif type == "code":
            code_content = "\n".join(block.strip().split("\n")[1:-1])
            pre_node = ParentNode("pre", children=[])
            code_node = ParentNode(tag, children=[])
            children = text_to_children(code_content)
            code_node.children.extend(children)
            pre_node.children.append(code_node)
            parent.children.append(pre_node)

        elif type in ["ordered_list", "unordered_list"]:
            list_node = ParentNode(tag, children=[])
            delimiter = r"\* |- " if type == "unordered_list" else r"\d. "
            split_list = re.split(delimiter, block)
            for item in split_list:
                if item.strip():
                    li_node = ParentNode("li", children=[])
                    children = text_to_children(item.strip())
                    li_node.children.extend(children)
                    list_node.children.append(li_node)
            parent.children.append(list_node)

        elif type == "quote":
            blockquote_node = ParentNode(tag, children=[])
            lines = block.split("\n")
            clean_lines = [line.lstrip("> ").strip() for line in lines]
            clean_block = " ".join(clean_lines)
            children = text_to_children(clean_block)
            blockquote_node.children.extend(children)
            parent.children.append(blockquote_node)

        else:
            nested_parent = ParentNode(tag, children=[])
            children = text_to_children(block)
            nested_parent.children.extend(children)
            parent.children.append(nested_parent)

    return parent
