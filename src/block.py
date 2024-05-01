from parentnode import ParentNode
from textnode import text_to_textnodes, text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown: str):
    split_blocks = markdown.strip(" ").split("\n\n")
    strip_blocks = []
    for block in split_blocks:
        if block != "":
            strip_lines = []
            lines = block.split("\n")
            for line in lines:
                if line != "":
                    strip_lines.append(line.strip())
            strip_blocks.append("\n".join(strip_lines))

    return strip_blocks


def block_to_block_type(markdown: str):
    if markdown.startswith("```") and markdown.endswith("```"):
        return block_type_code

    lines = markdown.split("\n")
    if (
        markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "####### "))
        and len(lines) == 1
    ):
        return block_type_heading

    block_type = block_type_paragraph
    order = 1
    firstLine = lines[0]

    if firstLine.startswith(">"):
        block_type = block_type_quote
    if firstLine.startswith(("* ", "- ")):
        block_type = block_type_unordered_list
    if firstLine.startswith(f"{order}. "):
        block_type = block_type_ordered_list
        order += 1

    for i in range(1, len(lines)):
        line = lines[i]
        line_type = None
        if line.startswith(">"):
            line_type = block_type_quote
        elif line.startswith(("* ", "- ")):
            line_type = block_type_unordered_list
        elif line.startswith(f"{order}. "):
            line_type = block_type_ordered_list
            order += 1
        else:
            return block_type_paragraph

        if line_type != block_type:
            return block_type_paragraph

    return block_type


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_ordered_list:
        return olist_to_html_node(block)
    if block_type == block_type_unordered_list:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block: str):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block: str):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block: str):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
