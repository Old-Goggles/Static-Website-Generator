import unittest
from textnode import TextNode, TextType
from split_nodes import *

def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

def test_split_image_at_start(self):
    node = TextNode("![image](https://example.com/pic.jpg) some text after", TextType.TEXT)
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("image", TextType.IMAGE, "https://example.com/pic.jpg"),
            TextNode(" some text after", TextType.TEXT),
        ],
        new_nodes,
    )

def test_split_image_at_end(self):
    node = TextNode("This is an ![end image](https://example.com/pic.jpg)", TextType.TEXT)
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is an ", TextType.TEXT),
            TextNode("end image", TextType.IMAGE, "https://example.com/pic.jpg"),
        ],
        new_nodes
    )

def test_split_image_with_non_text_nodes(self):
    text_node = TextNode("Text with ![image](https://example.com/pic.jpg)", TextType.TEXT)
    image_node = TextNode("existing image", TextType.IMAGE, "https://example.com/existing.jpg")
    link_node = TextNode("existing link", TextType.LINK, "https://example.com/existing")
    
    new_nodes = split_nodes_image([text_node, image_node, link_node])
    
    self.assertListEqual(
        [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/pic.jpg"),
            image_node,
            link_node,
        ],
        new_nodes,
    )

def test_split_image_no_images(self):
    node = TextNode("This is just plain text with no images", TextType.TEXT)
    new_nodes = split_nodes_image([node])
    self.assertListEqual([node], new_nodes)

def test_split_image_single_image(self):
    node = TextNode("Here is ![one image](https://example.com/pic.jpg) only", TextType.TEXT)
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("Here is ", TextType.TEXT),
            TextNode("one image", TextType.IMAGE, "https://example.com/pic.jpg"),
            TextNode(" only", TextType.TEXT),
        ],
        new_nodes,
    )

def test_split_image_adjacent_images(self):
    node = TextNode("![first](https://example.com/1.jpg)![second](https://example.com/2.jpg)", TextType.TEXT)
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("first", TextType.IMAGE, "https://example.com/1.jpg"),
            TextNode("second", TextType.IMAGE, "https://example.com/2.jpg"),
        ],
        new_nodes,
    )

def test_split_links(self):
    node = TextNode(
        "This is text with an [link](https://example.com) and another [second link](https://example2.com)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link", TextType.LINK, "https://example2.com"
            ),
        ],
        new_nodes,
    )

def test_split_image_no_links(self):
    node = TextNode("This is just plain text with no links", TextType.TEXT)
    new_nodes = split_nodes_link([node])
    self.assertListEqual([node], new_nodes)

def test_split_link_single_link(self):
    node = TextNode("Here is [one link](https://example.com) only", TextType.TEXT)
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("Here is ", TextType.TEXT),
            TextNode("one link", TextType.LINK, "https://example.com"),
            TextNode(" only", TextType.TEXT),
        ],
        new_nodes,
    )

def test_split_link_at_start(self):
    node = TextNode("[link](https://example.com) some text after", TextType.TEXT)
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" some text after", TextType.TEXT),
        ],
        new_nodes,
    )

def test_split_link_at_end(self):
    node = TextNode("This is a [end link](https://example.com)", TextType.TEXT)
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is a ", TextType.TEXT),
            TextNode("end link", TextType.LINK, "https://example.com"),
        ],
        new_nodes
    )

def test_split_link_with_non_text_nodes(self):
    text_node = TextNode("Text with [link](https://example.com)", TextType.TEXT)
    image_node = TextNode("existing image", TextType.IMAGE, "https://example.com/existing.jpg")
    link_node = TextNode("existing link", TextType.LINK, "https://example.com/existing")
    
    new_nodes = split_nodes_link([text_node, image_node, link_node])
    
    self.assertListEqual(
        [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            image_node,
            link_node,
        ],
        new_nodes,
    )

def test_split_link_adjacent_links(self):
    node = TextNode("[first](https://example.com)[second](https://example2.com)", TextType.TEXT)
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("first", TextType.LINK, "https://example.com"),
            TextNode("second", TextType.LINK, "https://example2.com"),
        ],
        new_nodes,
    )
