import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_node(self):
        node = HTMLNode(
            "p", 
            "hello world", 
            ["a", "b"], 
            {"href": "https://www.google.com","target": "_blank",}
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello world")
        self.assertIsInstance(node.children, list)
        
    def test_props(self):
        node = HTMLNode(
            "p", 
            "hello world", 
            ["a", "b"], 
            {"href": "https://www.google.com","target": "_blank",}
        )
        self.assertEqual(node.props["href"], "https://www.google.com")
        self.assertEqual(node.props["target"], "_blank")

    def test_props_to_html(self):
        node = HTMLNode(
            "p", 
            "hello world", 
            ["a", "b"], 
            {"href": "https://www.google.com","target": "_blank",}
        )
        string_props = node.props_to_html()
        self.assertEqual(string_props, "href=\"https://www.google.com\" target=\"_blank\" ")

class TestLeafNode(unittest.TestCase):
    def test_node(self):
        node = LeafNode(
            tag="p", 
            value="hello world", 
            props={"href": "https://www.google.com","target": "_blank",}
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello world") 
        self.assertEqual(node.props["href"], "https://www.google.com")
        self.assertEqual(node.props["target"], "_blank")

    def test_to_html(self):
        node = LeafNode(
            value="hello world",
            tag="p", 
            props={"href": "https://www.google.com","target": "_blank",}
        )
        to_html = node.to_html()
        self.assertEqual(to_html, "<p>hello world</p>")

    def test_to_html_null_tag(self):
        node = LeafNode(
            value="hello world"
        )
        to_html = node.to_html()
        self.assertEqual(to_html, "hello world")

if __name__ == "__main__":
    unittest.main()