from leafnode import LeafNode
import re
from extract_markdown import extract_markdown_images, extract_markdown_links

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == text_type_text:
        return LeafNode(value=text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode(tag="b", value=text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode(tag="i", value=text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    if text_node.text_type == text_type_link:
        return LeafNode(tag="img", props={"src": text_node.url, "alt": text_node.text})
    raise Exception(f"Invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes: TextNode, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if isinstance(old_node, TextNode) and old_node.text_type == text_type_text:
            split_text = old_node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception(
                    f"Invalid Markdown syntax:\n markdown: {old_node.text}\n delimiter: {delimiter}"
                )
            for i in range(len(split_text)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], old_node.text_type))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
        else:
            new_nodes.append(old_node)

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text != "":
            extracted_image_texts = extract_markdown_images(old_node.text)
            print(extracted_image_texts)
            # If there is no images
            if len(extracted_image_texts) == 0:
                new_nodes.append(old_node)
            else:
                index_image_texts = 0
                new_node = TextNode(
                    extracted_image_texts[index_image_texts][0],
                    text_type_image,
                    extracted_image_texts[index_image_texts][1],
                )
                new_nodes.append(new_node)
                index_image_texts += 1

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text != "":
            extracted_link_texts = extract_markdown_links(old_node.text)
            print(extracted_link_texts)
            # If there is no links
            if len(extracted_link_texts) == 0:
                new_nodes.append(old_node)
            else:
                index_link_texts = 0
                new_node = TextNode(
                    extracted_link_texts[index_link_texts][0],
                    text_type_link,
                    extracted_link_texts[index_link_texts][1],
                )
                new_nodes.append(new_node)
                index_link_texts += 1

    return new_nodes


def text_to_textnodes(text):
    textNodeWithInputText = [TextNode(text, text_type_text)]
    splitBoldTextNodes = split_nodes_delimiter(
        textNodeWithInputText, "**", text_type_bold
    )
    splitItalicTextNodes = split_nodes_delimiter(
        splitBoldTextNodes, "*", text_type_italic
    )
    splitCodeTextNodes = split_nodes_delimiter(
        splitItalicTextNodes, "`", text_type_code
    )
    splitImageNodes = split_nodes_image(splitCodeTextNodes)
    splitLinkNodes = split_nodes_link(splitImageNodes)

    return splitLinkNodes


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")
