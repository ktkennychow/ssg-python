import unittest

from textnode import (
    TextNode,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TestTextNode(unittest.TestCase):
    def test_eq_textnode(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_textnode_with_prop(self):
        node = TextNode("This is a text node", "light", "www.www.com")
        node2 = TextNode("This is a text node", "light", "www.www.com")
        self.assertEqual(node, node2)

    def test_not_eq_textnode(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "light", "www.www.com")
        self.assertNotEqual(node, node2)

    def test_eq_delimiter_code(self):
        old_nodes = [TextNode("This is text with a `code block` word", text_type_text)]
        delimiter = "`"
        text_type = text_type_code
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected_new_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

    def test_eq_delimiter_bold(self):
        old_nodes = [
            TextNode("This is text with a **bold block** word", text_type_text)
        ]
        delimiter = "**"
        text_type = text_type_bold
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected_new_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("bold block", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

    def test_eq_delimiter_italic(self):
        old_nodes = [
            TextNode("This is text with a *italic block* word", text_type_text)
        ]
        delimiter = "*"
        text_type = text_type_italic
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected_new_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("italic block", text_type_italic),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

    def test_eq_split_image_node(self):
        old_nodes = [
            TextNode(
                "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                text_type_text,
            ),
            TextNode(
                "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                text_type_text,
            ),
        ]
        new_nodes = split_nodes_image(old_nodes)
        expected_new_nodes = [
            TextNode("This is text with an ", text_type_text, None),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text, None),
            TextNode(
                "second image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
            TextNode("This is text with an ", text_type_text, None),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text, None),
            TextNode(
                "second image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

    def test_eq_split_link_node(self):
        old_nodes = [
            TextNode(
                "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
                text_type_text,
            ),
            TextNode(
                "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
                text_type_text,
            ),
        ]
        new_nodes = split_nodes_link(old_nodes)
        expected_new_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode("another link", text_type_link, "https://blog.boot.dev"),
            TextNode(" with text that follows", text_type_text),
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode("another link", text_type_link, "https://blog.boot.dev"),
            TextNode(" with text that follows", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

    def test_eq_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)
        expected_new_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(new_nodes, expected_new_nodes)


if __name__ == "__main__":
    unittest.main()
