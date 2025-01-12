import unittest

from block_text import (
    split_block,
    block_to_block_type,
    markdown_to_html_node
)

from htmlnode import ParentNode, LeafNode

class TestSplitBlock(unittest.TestCase):
    def test_split_block(self):
        text = (
            "# This is a heading\n"
            "\n"
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
            "\n"
            "* This is the first list item in a list block\n"
            "* This is a list item\n"
            "* This is another list item"
        )

        split_blocks = split_block(text)
        self.assertListEqual(
            [
                '# This is a heading', 
                'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
                '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
            ],
            split_blocks        
        )

    def test_split_blocks_no_splits(self):
        text = ""
        split_blocks = split_block(text)
        self.assertListEqual(
            split_blocks, 
            [""]
        )

class TestBlockToBlockType(unittest.TestCase):
    test_list = [
        "### This is a heading",
        "``` This is some code ```",
        "> first quote\n> second quote\n> third quote",
        "* first item\n* second item\n- third item", 
        "1. first item\n2. second item\n3. third item",
        "This is a paragraph. it has some **bold** text and some *italics*."
    ]
    def test_block_to_block_type(self):
        block_types = list(map(block_to_block_type, self.test_list)) 
        self.assertListEqual(
            [
                "heading",
                "code",
                "quote",
                "unordered_list",
                "ordered_list",
                "paragraph"
            ],
            block_types
        )

class TestMarkdownToHTMLNode(unittest.TestCase):
    paragraph = "This is some text with **bold** and `code`"
    h1 = "# This is a heading 1"
    h2 = "## This is a heading 2"
    h5_nest = "##### This is a **bold** heading"
    ul = "* elem 1\n* elem2\n* elem 3"
    ol = "1. elem 1\n2. elem2\n3. elem 3"
    code = "```sick code bruh```"
    blockquote = "> this is\n> part of a quote\n> that has an *italic* element"

    def test_paragraph(self):
        p = markdown_to_html_node(self.paragraph)
        comp = ParentNode("div", children=[
                ParentNode("p", children=[
                    LeafNode(tag=None, value="This is some text with "),
                    LeafNode(tag="b", value="bold"),
                    LeafNode(tag=None, value=" and "),
                    LeafNode(tag="code", value="code")
                    ]
                )]
            )
        self.assertEqual(comp, p)

    def test_h1(self):
        h1 = markdown_to_html_node(self.h1)
        comp = ParentNode("div", children=[
            ParentNode("h1", children=[
                LeafNode(tag=None, value="This is a heading 1")
            ])
        ])
        self.assertEqual(comp, h1)

    def test_h2(self):
        h2 = markdown_to_html_node(self.h2)
        comp = ParentNode("div", children=[
            ParentNode("h2", children=[
                LeafNode(tag=None, value="This is a heading 2")
            ])
        ])
        self.assertEqual(comp, h2)

    def test_h5(self):
        h5 = markdown_to_html_node(self.h5_nest)
        comp = ParentNode("div", children=[
            ParentNode("h5", children=[
                LeafNode(tag=None, value="This is a "),
                LeafNode(tag="b", value="bold"),
                LeafNode(tag=None, value=" heading")
            ])
        ])
        self.assertEqual(comp, h5)
# todo add more tests