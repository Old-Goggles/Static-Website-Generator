from blocktype import *

def block_to_block_type(markdown):
    count = 0
    for char in markdown:
        if char == "#":
            count += 1
        else:
            break
    if 1 <= count <= 6 and len(markdown) > count and markdown[count] == " ":
        return BlockType.HEADING
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    lines = markdown.splitlines()
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            break
    else:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    