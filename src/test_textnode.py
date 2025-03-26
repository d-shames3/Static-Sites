import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is text", TextType.ITALIC)
        self.assertEqual(node.text, "This is text")

    def test_type(self):
        node = TextNode("This is text", TextType.CODE)
        self.assertEqual(node.text_type.value, "code")

    def test_url(self):
        node = TextNode("This is text", TextType.IMAGE, "http://www.google.com")
        self.assertEqual(node.url, "http://www.google.com")

    def test_null_url(self):
        node = TextNode("This is text", TextType.CODE)
        self.assertEqual(node.url, None)

    def test_text_type_diff(self):
        node = TextNode("This is text", TextType.CODE)
        node2 = TextNode("This is text", TextType.ITALIC)
        self.assertNotEqual(node.text_type, node2.text_type)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_conversion(self):
        code_node = TextNode("This is code", TextType.CODE)
        converted = text_node_to_html_node(code_node)
        to_html = converted.to_html()
        self.assertEqual(to_html, "<code>This is code</code>")

        bold_node = TextNode("This is bold", TextType.BOLD)
        converted = text_node_to_html_node(bold_node)
        to_html = converted.to_html()
        self.assertEqual(to_html, "<b>This is bold</b>")

        italic_node = TextNode("This is italic", TextType.ITALIC)
        converted = text_node_to_html_node(italic_node)
        to_html = converted.to_html()
        self.assertEqual(to_html, "<i>This is italic</i>")


if __name__ == "__main__":
    unittest.main()
