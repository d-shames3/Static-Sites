import unittest
from site_generator import extract_title

class TestExtractTitile(unittest.TestCase):
    valid_markdown = "# This is the heading\n## Then this is heading 2\n* bullet list 1\n* bullet list two"
    invalid_markdown = "##### This is the heading\n## Then this is heading 2\n* bullet list 1\n* bullet list two"
    
    def test_valid_extract_title(self):
        valid_heading = extract_title(self.valid_markdown)
        self.assertEqual(
            "This is the heading",
            valid_heading
        )

    def test_invalid_extract_title(self):
        with self.assertRaises(Exception):
            extract_title(self.invalid_markdown)
            