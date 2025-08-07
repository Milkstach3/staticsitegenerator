from textnode import TextNode, TextType
import re

def text_to_textnodes(text) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_nodes = []
        parts = node.text.split(delimiter)
        
        if len(parts) % 2 == 0: raise ValueError("invalid markdown, formatted section not closed")
        
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(parts[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text) -> list:
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images


def extract_markdown_links(text) -> list:
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def split_nodes_image(old_nodes) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
    
def split_nodes_image_0(old_nodes):
    new_nodes = []
    # lyst = re.findall(r"!\[(.*?)\]\((.*?)\)", old_nodes)
    # print(lyst)

    for node in old_nodes:
        
        split_nodes = []
        # parts = node.text.split(delimiter)
        parts = re.findall(r"!\[(.*?)\]\((.*?)\)", node.text)
        cleaned = re.sub(r'!\[(.*?)\]\((.*?)\)', '', node.text)

        # print(f"IMAGE PARTS: {parts}")
        
        # if len(parts) % 2 == 0: raise ValueError("invalid markdown, formatted section not closed")
        for p in parts:
            i = 0
            for i in range(len(p)):
                if p[0] == "":
                    split_nodes.append(TextNode(parts[1], TextType.TEXT))
                    split_nodes.append(TextNode(parts[2], TextType.IMAGE))
                else:
                    split_nodes.append(TextNode(parts[0], TextType.TEXT))
                    split_nodes.append(TextNode(parts[1], TextType.TEXT))                
                    split_nodes.append(TextNode(parts[2], TextType.IMAGE))
        # print(f"IMAGE SPLIT NODES: {split_nodes}")    
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link_0(old_nodes):   
    # lyst = re.findall(r"\[(.*?)\]\((.*?)\)", old_nodes)
    new_nodes = []
    # lyst = re.findall(r"!\[(.*?)\]\((.*?)\)", old_nodes)
    # print(lyst)

    for node in old_nodes:
        
        split_nodes = []
        # parts = node.text.split(delimiter)
        parts = re.findall(r"(.*?)\[(.*?)\]\((.*?)\)", node.text)
        # print(f"LINK PARTS: {parts}")
        
        # if len(parts) % 2 == 0: raise ValueError("invalid markdown, formatted section not closed")

        for p in parts:
            if p[0] == "":
                split_nodes.append(TextNode(parts[1], TextType.TEXT))
                split_nodes.append(TextNode(parts[2], TextType.LINK))
            else:
                split_nodes.append(TextNode(parts[0], TextType.TEXT))
                split_nodes.append(TextNode(parts[1], TextType.TEXT))                
                split_nodes.append(TextNode(parts[2], TextType.LINK))
        # print(f"LINK SPLIT NODES: {split_nodes}")
        new_nodes.extend(split_nodes)
    return new_nodes