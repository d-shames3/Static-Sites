import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_node(self):
        node = HTMLNode(
            "p",
            "hello world",
            ["a", "b"],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello world")
        self.assertIsInstance(node.children, list)

    def test_props(self):
        node = HTMLNode(
            "p",
            "hello world",
            ["a", "b"],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(node.props["href"], "https://www.google.com")
        self.assertEqual(node.props["target"], "_blank")

    def test_props_to_html(self):
        node = HTMLNode(
            "p",
            "hello world",
            ["a", "b"],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        string_props = node.props_to_html()
        self.assertEqual(string_props, ' href="https://www.google.com" target="_blank"')


class TestLeafNode(unittest.TestCase):
    def test_node(self):
        node = LeafNode(
            tag="p",
            value="hello world",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello world")
        self.assertEqual(node.props["href"], "https://www.google.com")
        self.assertEqual(node.props["target"], "_blank")

    def test_to_html(self):
        node = LeafNode(
            value="hello world",
            tag="p",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        to_html = node.to_html()
        self.assertEqual(
            to_html, '<p href="https://www.google.com" target="_blank">hello world</p>'
        )

    def test_to_html_null_tag(self):
        node = LeafNode(value="hello world")
        to_html = node.to_html()
        self.assertEqual(to_html, "hello world")


class TestParentNode(unittest.TestCase):
    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(len(node.children), 4)
        self.assertEqual(node.props["href"], "https://www.google.com")

    def test_recursive_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        to_html = node.to_html()
        self.assertEqual(
            to_html,
            '<p href="https://www.google.com" target="_blank"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>',
        )

    def test_recursive_to_html_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_recursive_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode(tag="b", value="test")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_recursive_to_html_nested_parents(self):
        node = ParentNode(
            "p",
            [
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                ParentNode(
                    "code",
                    [
                        LeafNode(tag="i", value="italic text"),
                        LeafNode(tag=None, value="Normal text"),
                    ],
                ),
            ],
        )
        to_html = node.to_html()
        self.assertEqual(
            to_html,
            "<p><b>Bold text</b>Normal text<code><i>italic text</i>Normal text</code></p>",
        )

    def test_recursive_html_empty_string(self):
        node = ParentNode(
            None,
            [
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                ParentNode(
                    "code",
                    [
                        LeafNode(tag="i", value="italic text"),
                        LeafNode(tag=None, value="Normal text"),
                    ],
                ),
            ],
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_recursive_html_empty_child_string(self):
        node = ParentNode(
            "b",
            [
                LeafNode(tag="b", value=None),
                LeafNode(tag=None, value="Normal text"),
                ParentNode(
                    "code",
                    [
                        LeafNode(tag="i", value="italic text"),
                        LeafNode(tag=None, value="Normal text"),
                    ],
                ),
            ],
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_recursive_html_invalid_child(self):
        node = ParentNode(
            "b",
            [
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                ParentNode(
                    "code",
                    [
                        LeafNode(tag="i", value="italic text"),
                        {"tag": None, "value": "Normal text"},
                    ],
                ),
            ],
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_recursive_html_deep_nesting(self):
        node = ParentNode(
            "b",
            [
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                ParentNode(
                    "code",
                    [
                        LeafNode(tag="i", value="italic text"),
                        ParentNode(
                            "blockquote",
                            [
                                LeafNode(tag="title", value="test title"),
                                ParentNode(
                                    "body",
                                    [
                                        LeafNode(tag="link", value="www.test.com"),
                                        LeafNode(tag="head", value="this is a heading"),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
        to_html = node.to_html()
        self.assertEqual(
            to_html,
            "<b><b>Bold text</b>Normal text<code><i>italic text</i><blockquote><title>test title</title><body><link>www.test.com</link><head>this is a heading</head></body></blockquote></code></b>",
        )


if __name__ == "__main__":
    unittest.main()
