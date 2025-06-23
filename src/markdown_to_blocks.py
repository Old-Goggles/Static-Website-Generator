import re

def markdown_to_blocks(markdown):
    blocks = re.split(r'\n\s*\n', markdown)
    return [block.strip() for block in blocks if block.strip() != ""]