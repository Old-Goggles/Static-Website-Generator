from textnode import TextNode, TextType
from extract_markdown import *

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            result = extract_markdown_images(node.text)
            if result == []:
                new_nodes.append(node)
            else:
                current_text = node.text
                for alt_text, url in result:
                    markdown = f"![{alt_text}]({url})"
                    split_text = current_text.split(markdown, 1)
                    if split_text[0] != "":
                        new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                    current_text = split_text[1]
                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            result = extract_markdown_links(node.text)
            if result == []:
                new_nodes.append(node)
            else:
                current_text = node.text
                for alt_text, url in result:
                    markdown = f"[{alt_text}]({url})"
                    split_text = current_text.split(markdown, 1)
                    if split_text[0] != "":
                        new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                    current_text = split_text[1]
                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes