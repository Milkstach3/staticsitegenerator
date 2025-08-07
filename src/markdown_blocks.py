from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_html_node(markdown: str) -> ParentNode:
    mark_blocks: list[str] = markdown_to_blocks(markdown)
    lyst_of_parent_nodes: list[ParentNode] = []
    parent_node: ParentNode
    for block in mark_blocks:
        block_type: BlockType = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                parent_node = heading_html_node(block)

            case BlockType.CODE:
                parent_node = code_html_node(block) 

            case BlockType.QUOTE:
                parent_node = quote_html_node(block)

            case BlockType.OLIST:
                parent_node = ordered_list_html_node(block, True)

            case BlockType.ULIST:
                parent_node = ordered_list_html_node(block, False)
                
            case BlockType.PARAGRAPH:
                parent_node = paragraph_html_node(block)

            case _:
                raise ValueError(f"Unknown block type: {block_type}")

        lyst_of_parent_nodes.append(parent_node)
    
    div_node = ParentNode(tag="div", children=lyst_of_parent_nodes)
    return div_node   

def text_to_children(block) -> list[LeafNode]:
    if not block:
        raise ValueError("text_to_children: block cannot be empty")
    leaf_node_lyst: list[LeafNode] = []
    text_nodes: list[TextNode] = text_to_textnodes(block)

    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        leaf_node = LeafNode(tag=html_node.tag, value=html_node.value, props=html_node.props)
        leaf_node_lyst.append(leaf_node)
    return leaf_node_lyst

def heading_html_node(block) -> ParentNode:
    h_count = heading_count(block)
    # print(f"HEADING TEXT:::::::::: '{block[h_count+1:]}'")
    leaf_node_lyst: list[LeafNode] = text_to_children(block[h_count+1:])
    parent_node: ParentNode = ParentNode(tag=f"h{h_count}", children=leaf_node_lyst)
    return parent_node


def code_html_node(block: str) -> ParentNode:
    # Remove the ``` markers but preserve internal whitespace
    lines = block.split('\n')
    # Remove first and last lines if they contain ```
    if lines[0].strip().startswith('```'):
        lines = lines[1:]
    if lines and lines[-1].strip().endswith('```'):
        lines = lines[:-1]
    
    # Join back with newlines, preserving the original formatting
    clean_block = '\n'.join(lines)
    if clean_block and not clean_block.endswith('\n'):
        clean_block += '\n'
    leaf_node = LeafNode(tag="code", value=clean_block)
    return ParentNode(tag="pre", children=[leaf_node])

def quote_html_node(block) -> ParentNode:
    lines = block.split('\n')
    quote_lines = []
    for line in lines:
        # Remove "> " from the beginning of each line
        if line.startswith('> '):
            quote_lines.append(line[2:])
        elif line.startswith('>'):
            quote_lines.append(line[1:])
    
    # Join all lines back together with spaces (not newlines)
    quote_text = ' '.join(quote_lines).strip()
    parent_node = ParentNode(tag="blockquote", children=text_to_children(quote_text))
    return parent_node

def ordered_list_html_node(block: str, ordered: bool = True)-> ParentNode:
    list_items: list[ParentNode] = []
    lines = block.split("\n")
    content: str = ""

    for line in lines:
        if line.strip() == "":
            continue

        if ordered: content = line[3:]
        else:       content = line[2:]

        item_children = text_to_children(content)
        li_node = ParentNode(tag="li", children=item_children)
        list_items.append(li_node)

    if not list_items:
        if(ordered): raise ValueError("invalid markdown: no items in ordered list")
        else: raise ValueError("invalid markdown: no items in unordered list")

    tag = "ol" if ordered else "ul"
    parent_node = ParentNode(tag=tag, children=list_items)
    return parent_node

def paragraph_html_node(block) -> ParentNode:
    parent_node: ParentNode = ParentNode(tag="p", children=[])
    paragraph_text = block.replace('\n', ' ').strip()
    lyst_of_children: list[LeafNode] = text_to_children(paragraph_text)
    parent_node.children = lyst_of_children
    return parent_node

def heading_count(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    return count

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    blocks = []
    for block in split_markdown:
        strip_block = block.strip()
        if strip_block == "":
            continue
        blocks.append(strip_block)
    return blocks

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    split_block = block.split("\n")
    if len(split_block) > 1 and block.startswith("```"):
        return BlockType.CODE
    first_chars = [line[0] for line in split_block if line]
    set_of_first_chars = set(first_chars)
    if len(set_of_first_chars) == 1:
        element = next(iter(set_of_first_chars))
        if element == ">":
            return BlockType.QUOTE
        if element == "-":
            return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in split_block:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST

    return BlockType.PARAGRAPH