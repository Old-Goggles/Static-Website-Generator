import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_equrl(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://www.example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, url="https://www.example.com")
        self.assertEqual(node, node2)

    def test_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://www.example.org")
        node2 = TextNode("This is a text node", TextType.BOLD, url="https://www.example.com")
        self.assertNotEqual(node, node2)

    def test_nourl(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD, url="https://www.example.com")
        self.assertNotEqual(node, node2)


        


if __name__ == "__main__":
    unittest.main()
