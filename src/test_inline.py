import unittest
from inline_text import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link
)
from textnode import TextNode, TextType

class TestSplitDelimiter(unittest.TestCase):
    def test_split_delimiter(self):
        node_list = [TextNode("This is some normal and then `code` text", TextType.NORMAL)]
        split_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)
        self.assertEqual(split_nodes, [
            TextNode("This is some normal and then ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.NORMAL)
        ])

    def test_split_delimiter_multiple_nodes(self):
        node_list = [TextNode("This is some normal and then **bold** text", TextType.NORMAL), TextNode("**Bold** to start followed by normal text", TextType.NORMAL)]
        split_nodes = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        self.assertEqual(split_nodes, [
            TextNode("This is some normal and then ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
            TextNode("Bold", TextType.BOLD),
            TextNode(" to start followed by normal text", TextType.NORMAL)
        ])
        
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.NORMAL
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.NORMAL),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.NORMAL
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
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
                ("obi wan", "https://ilimgur.com/fJrM4Vk.jepg")
            ]
        )

    def test_extract_markdown_links(self):
        links = extract_markdown_links(self.string)
        self.assertListEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        )

    def test_split_nodes_image(self):
        node = TextNode("This is text with an ![image](https://www.image.com) that we are testing", TextType.NORMAL)
        split_images = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://www.image.com"),
                TextNode(" that we are testing", TextType.NORMAL)
            ],
            split_images,
        )

    def test_multiple_split_nodes_image(self):
        node = TextNode("This is text with an ![image](https://www.image.com) that we are testing and ![here](https://www.another.com) is another and a [link](https://www.link.com)", TextType.NORMAL)
        split_images = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://www.image.com"),
                TextNode(" that we are testing and ", TextType.NORMAL),
                TextNode("here", TextType.IMAGE, "https://www.another.com"),
                TextNode(" is another and a [link](https://www.link.com)", TextType.NORMAL)
            ],
            split_images,
        )

    def test_split_nodes_link(self):
        node = TextNode("This is text with an [link](https://www.link.com) that we are testing", TextType.NORMAL)
        split_links = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://www.link.com"),
                TextNode(" that we are testing", TextType.NORMAL)
            ],
            split_links,
        )

    def test_multiple_split_nodes_image(self):
        node = TextNode("This is text with an [link](https://www.link.com) that we are testing and [here](https://www.another.com) is another and a ![image](https://www.image.com)", TextType.NORMAL)
        split_links = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://www.link.com"),
                TextNode(" that we are testing and ", TextType.NORMAL),
                TextNode("here", TextType.LINK, "https://www.another.com"),
                TextNode(" is another and a ![image](https://www.image.com)", TextType.NORMAL)
            ],
            split_links,
        )