import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_attributes(self):
        node = HTMLNode("a", None, None, {"href": "https://test.com", "target": "_blank"})
        result = node.props_to_html()
        expected = ' href="https://test.com" target="_blank"'
        self.assertEqual(result, expected)

    def test_props_to_html_no_props(self):
        node = HTMLNode("b", None, None, None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test__repr__(self):
        node = HTMLNode("c", None, None, {"href": "https://test.com", "target": "_blank"})
        result = repr(node)
        expected = 'HTMLNode(tag=c, value=None, children=None, props={\'href\': \'https://test.com\', \'target\': \'_blank\'})'
        self.assertEqual(result, expected)

    def test__repr__with_value(self):
        node = HTMLNode("d", "Example Value", None, None)
        result = repr(node)
        expected = "HTMLNode(tag=d, value=Example Value, children=None, props=None)"
        self.assertEqual(result, expected)

    def test__repr__with_tag(self):
        node = HTMLNode(None, "Example", None, None)
        result = repr(node)
        expected = "HTMLNode(tag=None, value=Example, children=None, props=None)"
        self.assertEqual(result, expected)

    def test__repr__with_children(self):
        child = HTMLNode("strong", "child", None, None)
        node = HTMLNode("f", None, [child], None)
        result = repr(node)
        expected = "HTMLNode(tag=f, value=None, children=[HTMLNode(tag=strong, value=child, children=None, props=None)], props=None)"
        self.assertEqual(result, expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_value(self):
        node = LeafNode(None, "Example", None)
        self.assertEqual(node.to_html(), "Example")

    def test_leaf_with_props(self):
        node = LeafNode("a", "Example", {"href": "https://test.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://test.com\">Example</a>")

    def test_leaf_no_value_raises_error(self):
        node = LeafNode("b", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            child_node = LeafNode("c", "Example", None)
            parent_node = ParentNode(None, [child_node])
            parent_node.to_html()

    def test_no_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("d", None,)
            parent_node.to_html()
