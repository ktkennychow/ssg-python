from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=""):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("tag is missing")
        if self.children == None:
            raise ValueError("children is missing")

        children_htmls = []
        for child in self.children:
            children_htmls.append(child.to_html())

        children_html_string = "".join(children_htmls)
        family_html_string = f"<{self.tag}>{children_html_string}</{self.tag}>"

        return family_html_string
