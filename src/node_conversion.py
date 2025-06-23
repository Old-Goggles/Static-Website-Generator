import re
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from extract_markdown import *
from split_delimiter import split_nodes_delimiter
from split_nodes import split_nodes_image, split_nodes_link
from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import *


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src":text_node.url, "alt":text_node.text})
    else:
        raise Exception("invalid text type")

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        block_text = block

        if block_type != BlockType.CODE:
            if block_type == BlockType.PARAGRAPH:
                tag = "p"
                paragraph_text = " ".join(line.strip() for line in block_text.splitlines())
                child_nodes = text_to_children(paragraph_text)

            elif block_type == BlockType.QUOTE:
                quote_groups = []
                current_group = []
                for line in block_text.splitlines():
                    cleaned = line.lstrip()
                    if cleaned.strip() == ">" or cleaned == "":
                        if current_group:
                            quote_groups.append(current_group)
                            current_group = []
                    elif cleaned.startswith(">"):
                        current_group.append(cleaned[1:].lstrip())
                if current_group:
                    quote_groups.append(current_group)

                for group in quote_groups:
                    quote_text = " ".join(group).strip()
                    child_nodes = text_to_children(quote_text)
                    block_html_node = ParentNode("blockquote", child_nodes)
                    html_nodes.append(block_html_node)
                continue
            
            elif block_type == BlockType.UNORDERED_LIST:
                tag = "ul"
                child_nodes = []
                for line in block_text.splitlines():
                    stripped = line.lstrip()
                    if not stripped.startswith("- "):
                        continue
                    item_text = stripped[2:]
                    li_nodes = text_to_children(item_text)
                    child_nodes.append(ParentNode("li", li_nodes))
                block_html_node = ParentNode(tag, child_nodes)
                html_nodes.append(block_html_node)
                continue
                
            elif block_type == BlockType.ORDERED_LIST:
                tag = "ol"
                child_nodes = []
                for line in block_text.splitlines():
                    stripped = line.lstrip()
                    match = re.match(r'^\d+\.\s+(.+)', stripped)
                    if not match:
                        continue  
                    item_text = match.group(1).strip()
                    if not item_text:
                        continue  
                    li_nodes = text_to_children(item_text)
                    child_nodes.append(ParentNode("li", li_nodes))
                block_html_node = ParentNode("ol", child_nodes)
                html_nodes.append(block_html_node)
                continue

            elif block_type == BlockType.HEADING:
                heading_level = 0
                index = 0
                while index < len(block_text) and block_text[index] == "#":
                     heading_level += 1 
                     index += 1   
                tag = f"h{heading_level}"
                cleaned_text = block_text[index:].strip()
                child_nodes = text_to_children(cleaned_text)

            else:
                 raise ValueError(f"Unknown block type: {block_type}")
            block_html_node = ParentNode(tag, child_nodes)
            html_nodes.append(block_html_node)

        else:
            cleaned_code_text = block_text[3:-3]
            cleaned_code_text = cleaned_code_text.lstrip('\n')
            lines = cleaned_code_text.splitlines()
            lines = [line[4:] if line.startswith("    ") else line for line in lines]
            cleaned_code_text = "\n".join(lines)
            code_text_node = TextNode(cleaned_code_text, TextType.CODE)
            code_html_node = text_node_to_html_node(code_text_node)
            pre_html_node = ParentNode("pre", [code_html_node])
            html_nodes.append(pre_html_node)

    return ParentNode("div", html_nodes)
