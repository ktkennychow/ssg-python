import re


def extract_markdown_images(text):
    list_altText_url: list[tuple] = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return list_altText_url


def extract_markdown_links(text):
    list_anchorText_url: list[tuple] = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return list_anchorText_url
