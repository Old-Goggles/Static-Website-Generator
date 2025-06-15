import unittest
from textnode import TextNode, TextType
from split_delimiter import *

class TestSplitDelimiter(unittest.TestCase):
    def test_single_delimited_word(self):
        input_nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimited_sections(self):
        input_nodes = [TextNode("A **bold** and **strong** word", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("strong", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_delimiters_at_start_and_end(self):
        input_nodes = [TextNode("**loud**", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        expected = [TextNode("loud", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_no_delimiters_present(self):
        input_nodes = [TextNode("Plain text", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        expected = [TextNode("Plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_unmatched_delimiters(self):
        input_nodes = [TextNode("Oh no, an **unclosed bold!", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        self.assertIn("Invalid Markdown syntax", str(context.exception))

        