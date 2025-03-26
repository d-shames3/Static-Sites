import unittest
from inline_text import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitDelimiter(unittest.TestCase):
    def test_split_delimiter(self):
        node_list = [TextNode("This is some TEXT and then `code` text", TextType.TEXT)]
        split_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)
        self.assertEqual(
            split_nodes,
            [
                TextNode("This is some TEXT and then ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_delimiter_multiple_nodes(self):
        node_list = [
            TextNode("This is some TEXT and then **bold** text", TextType.TEXT),
            TextNode("**Bold** to start followed by TEXT text", TextType.TEXT),
        ]
        split_nodes = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        self.assertEqual(
            split_nodes,
            [
                TextNode("This is some TEXT and then ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("Bold", TextType.BOLD),
                TextNode(" to start followed by TEXT text", TextType.TEXT),
            ],
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestMarkdownLinkImageExtraction(unittest.TestCase):
    string = """
                blahblah blah blah asd;fkljasldj@#DS![rick roll](https://i.imgur.com/aKa0qIh.gif)aj;sdfadkslblah blah blah![obi wan](https://ilimgur.com/fJrM4Vk.jepg)asd;jfa302309blah blah blah
                [to boot dev](https://www.boot.dev) a;jsdfakhb;a;blahblah
                a;asd;fajk;i23[to youtube](https://www.youtube.com/@bootdotdev)!@#(*Sblahblah
            """

    def test_extract_markdown_images(self):
        images = extract_markdown_images(self.string)
        self.assertListEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKa0qIh.gif"),
                ("obi wan", "https://ilimgur.com/fJrM4Vk.jepg"),
            ],
        )

    def test_extract_markdown_links(self):
        links = extract_markdown_links(self.string)
        self.assertListEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://www.image.com) that we are testing",
            TextType.TEXT,
        )
        split_images = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://www.image.com"),
                TextNode(" that we are testing", TextType.TEXT),
            ],
            split_images,
        )

    def test_multiple_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://www.image.com) that we are testing and ![here](https://www.another.com) is another and a [link](https://www.link.com)",
            TextType.TEXT,
        )
        split_images = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://www.image.com"),
                TextNode(" that we are testing and ", TextType.TEXT),
                TextNode("here", TextType.IMAGE, "https://www.another.com"),
                TextNode(
                    " is another and a [link](https://www.link.com)", TextType.TEXT
                ),
            ],
            split_images,
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with an [link](https://www.link.com) that we are testing",
            TextType.TEXT,
        )
        split_links = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.link.com"),
                TextNode(" that we are testing", TextType.TEXT),
            ],
            split_links,
        )

    def test_multiple_split_nodes_link(self):
        node = TextNode(
            "This is text with an [link](https://www.link.com) that we are testing and [here](https://www.another.com) is another and a ![image](https://www.image.com)",
            TextType.TEXT,
        )
        split_links = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.link.com"),
                TextNode(" that we are testing and ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://www.another.com"),
                TextNode(
                    " is another and a ![image](https://www.image.com)", TextType.TEXT
                ),
            ],
            split_links,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_nodes,
        )

    def test_text_to_text_nodes_empty_string(self):
        text = ""
        text_nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("", TextType.TEXT)], text_nodes)

    def test_text_to_text_nodes_nested(self):
        text = "**bold text with *italics* nested inside**"
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("bold text with *italics* nested inside", TextType.BOLD)],
            text_nodes,
        )

    def test_text_to_text_nodes_missing_closing_delim(self):
        text = "`Code text that is missing a close"

        with self.assertRaises(Exception):
            text_to_textnodes(text)

        text = "**Bold text with one close*"

        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_text_to_text_nodes_missing_urls(self):
        text = "[link with no url]"
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("[link with no url]", TextType.TEXT)], text_nodes
        )

        text = "![image with no url]"
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("![image with no url]", TextType.TEXT)], text_nodes
        )
