from htmlnode import HTMLNode
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props={}):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError()
        if self.tag == None:
            return f"{self.value}"

        props_list = []
        for key, value in self.props.items():
            props_list.append(f" {key}=\"{value}\"")
        html_props = "".join(props_list)
        

        html = f"<{self.tag}{html_props}>{self.value}</{self.tag}>"
        return html