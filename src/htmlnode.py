class HTMLNode():
    def __init__(self,tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value 
        self.children = children 
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_string = ""
        for key, value in self.props.items():
            props_string += f"{key}=\"{value}\" "
        return props_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(value=value, tag=tag, props=props, children=[])

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag == None or self.tag == "":
            return f"{self.value}"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props, value="")

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("All parent nodes must have a tag")
        elif self.children == None or self.children == []:
            raise ValueError("All parent nodes must have children nodes")
        else:
            start_html_string = f"<{self.tag}>"
            end_html_string = f"</{self.tag}>"
            for child in self.children:
                if isinstance(child, HTMLNode):
                    start_html_string += child.to_html()
                else:
                    raise ValueError("Child must be subclass of html node")
            return start_html_string + end_html_string
        