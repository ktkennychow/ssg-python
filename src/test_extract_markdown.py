import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_eq1(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        extracted_images_text = extract_markdown_images(text)

        self.assertEqual(
            extracted_images_text,
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "another",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
            ],
        )

    def test_eq2(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        extracted_links_text = extract_markdown_links(text)

        self.assertEqual(
            extracted_links_text,
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )

    def test_eq3(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another) and [another](https://www.example.com/another)"
        extracted_links_text = extract_markdown_links(text)

        self.assertEqual(
            extracted_links_text,
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
                ("another", "https://www.example.com/another"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
