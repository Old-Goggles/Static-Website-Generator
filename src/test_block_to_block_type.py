import unittest
from block_to_block_type import *

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading_single_hash(self):
        heading = "# This is a heading"
        result = block_to_block_type(heading)
        expected = BlockType.HEADING
        self.assertEqual(result, expected)

    def test_block_to_block_type_heading_multi_hash(self):
        heading = "#### This is also a heading"
        result = block_to_block_type(heading)
        expected = BlockType.HEADING
        self.assertEqual(result, expected)

    def test_block_to_block_type_heading_too_many_hash(self):
        heading = "########### This is not a heading"
        result = block_to_block_type(heading)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_block_to_block_type_code(self):
        code = "``` this is code block type ```"
        result = block_to_block_type(code)
        expected = BlockType.CODE
        self.assertEqual(result, expected)

    def test_block_to_block_type_no_end_ticks(self):
        code = "``` this is not code block type"
        result = block_to_block_type(code)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_block_to_block_type_bad_number_of_ticks(self):
        code = "`` this is not code block type ``"
        result = block_to_block_type(code)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_block_to_block_type_quote(self):
        quote = "> This is a quote"
        result = block_to_block_type(quote)
        expected = BlockType.QUOTE
        self.assertEqual(result, expected)

    def test_block_to_block_type_multiline_quote(self):
        quote = "> This is a quote\n> this quote\n> is on more than one line"
        result = block_to_block_type(quote)
        expected = BlockType.QUOTE
        self.assertEqual(result, expected)

    def test_block_to_block_type_not_a_quote(self):
        quote = "This is not a quote\n> because the first line\n> does not start with >"
        result = block_to_block_type(quote)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_block_to_block_type_unordered_list(self):
        list = "- This is an unordered list"
        result = block_to_block_type(list)
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(result, expected)

    def test_block_to_block_type_multiline_unordered_list(self):
        list = "- This is an unordered list\n- is on more than one line\n- this list"
        result = block_to_block_type(list)
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(result, expected)

    def test_block_to_block_type_not_an_unordered_list(self):
        list = "This is not an unordered list\n_ because the first line\n> does not start with - "
        result = block_to_block_type(list)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list(self):
        list = "1. this is an ordered list"
        result = block_to_block_type(list)
        expected = BlockType.ORDERED_LIST
        self.assertEqual(result, expected)

    def test_block_to_block_type_multiline_ordered_list(self):
        list = "1. this is an ordered list\n2. because each of its lines\n3. follow the rules"
        result = block_to_block_type(list)
        expected = BlockType.ORDERED_LIST
        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list_no_number(self):
        list = "this is not an ordered list\n because someone forgot the 1. and 2."
        result = block_to_block_type(list)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_block_to_block_type_paragraph(self):
        text = "This is just a regular paragraph with no special formatting."
        result = block_to_block_type(text)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)