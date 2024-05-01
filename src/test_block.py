import unittest

from block import markdown_to_blocks, block_to_block_type

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


class TestBlock(unittest.TestCase):
    def test_eq_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph




            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items
            """
        blocks = markdown_to_blocks(md)
        expected_blocks = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertEqual(
            expected_blocks,
            blocks,
        )

    def test_eq_block_to_block_type_ul(self):
        md = "* This is an unordered list\n* with items"

        block_type = block_to_block_type(md)
        expected_block_type = block_type_unordered_list

        self.assertEqual(
            expected_block_type,
            block_type,
        )

    def test_eq_block_to_block_type_h(self):
        md = "### This is a heading"

        block_type = block_to_block_type(md)
        expected_block_type = block_type_heading

        self.assertEqual(
            expected_block_type,
            block_type,
        )

    def test_eq_block_to_block_type_ol(self):
        md = "1. This is an ordered list\n2. with items"

        block_type = block_to_block_type(md)
        expected_block_type = block_type_ordered_list

        self.assertEqual(
            expected_block_type,
            block_type,
        )

    def test_eq_block_to_block_type_code(self):
        md = '``` This = "a code block" ```'

        block_type = block_to_block_type(md)
        expected_block_type = block_type_code

        self.assertEqual(
            expected_block_type,
            block_type,
        )

    def test_eq_block_to_block_type_quote(self):
        md = ">This is a quote\n> This is also a quote"

        block_type = block_to_block_type(md)
        expected_block_type = block_type_quote

        self.assertEqual(
            expected_block_type,
            block_type,
        )

    def test_eq_block_to_block_type_paragraph(self):
        md = "This is just a regular paragraph"

        block_type = block_to_block_type(md)
        expected_block_type = block_type_paragraph

        self.assertEqual(
            expected_block_type,
            block_type,
        )


if __name__ == "__main__":
    unittest.main()
