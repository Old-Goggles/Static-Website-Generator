import unittest
from extract_markdown import*

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            """This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)
            This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"""
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png"),
             ("image", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_extract_markdown_images_no_images(self):
        text_without_images = "This text has no images in it."
        matches = extract_markdown_images(text_without_images)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_single(self):
        text_with_one_link = "Check out this [cool site](https://boot.dev)."
        matches = extract_markdown_links(text_with_one_link)
        self.assertListEqual([('cool site', 'https://boot.dev')], matches)

    def test_extract_markdown_links_multiple(self):
        links = """This is an example [example](https://example.com)
                This is also an example [example too](https://lameexample.com)"""
        matches = extract_markdown_links(links)
        self.assertListEqual(
            [('example', 'https://example.com'),
             ('example too', 'https://lameexample.com')], matches
        )

    def test_extract_markdown_links_no_links(self):
        links = "Where are the Links"
        matches = extract_markdown_links(links)
        self.assertListEqual([], matches)