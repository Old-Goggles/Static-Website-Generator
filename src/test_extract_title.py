import unittest
from extract_title import *

class TestExtractTitle(unittest.TestCase):
    def test_no_title(self):
        md = "this is not a title"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title(self):
        md = "# Hello World"
        result = extract_title(md)
        expected = "Hello World"
        self.assertEqual(result, expected)