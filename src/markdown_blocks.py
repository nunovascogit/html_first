from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in raw_blocks:
        cleaned_block = block.strip()
        if cleaned_block != "":
            filtered_blocks.append(cleaned_block)

    return filtered_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lines) >= 2 and lines[0] == "```" and lines[-1] ==  "```":
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        current_number = 1
        for line in lines:
            prefix = f"{current_number}. "
            if not line.startswith(prefix):
                return BlockType.PARAGRAPH
            current_number += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)                 
 
        html_node = create_block_node(block, block_type)
        children.append(html_node)
#all block nodes children under a single parent
    return ParentNode("div", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def create_block_node(block, block_type):
    if block_type == BlockType.CODE:
        content = block.strip("`").strip()
        text_node = TextNode(content, TextType.CODE)
        raw_code_leaf = text_node_to_html_node(text_node)
        code_parent = ParentNode("code", [raw_code_leaf])
        return ParentNode("pre", [code_parent])

    if block_type == BlockType.UNORDERED_LIST:
    #process each list item ('* ' or '- ')
        items = block.split("\n")
        li_nodes = []
        for item in items:
            text_content = item[2:]
            children = text_to_children(text_content)
            li_nodes.append(ParentNode("li", text_to_children(text_content)))
        return ParentNode("ul", li_nodes)

    if block_type == BlockType.ORDERED_LIST:
        items = block.split("\n")
        li_nodes = []
        for item in items:
            start_index = item.find(". ") + 2
            text_content = item[start_index:]
            li_nodes.append(ParentNode("li", text_to_children(text_content)))
        return ParentNode("ol", li_nodes)

    if block_type == BlockType.HEADING:
        level = 0
        for char in block:
            if char == "#": level += 1
            else: break
        content = block[level + 1:].strip()
        return ParentNode(f"h{level}", text_to_children(content))


    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            if not line.startswith(">"):
                raise ValueError("Invalid quote block")
            new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
        return ParentNode("blockquote", text_to_children(content))

    return ParentNode("p", text_to_children(block.replace("\n", " ")))    
