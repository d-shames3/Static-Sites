import unittest

from block_text import (
    split_block,
    block_to_block_type
)

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
