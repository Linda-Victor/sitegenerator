class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
            raise NotImplementedError
        
    def props_to_html(self):
            final_html = ''
            if self.props == None:
                  return final_html
            for prop in self.props:
                final_html += f' {prop}="{self.props[prop]}"'
            return final_html

    def __repr__(self):
            return f'HTMLNode: {self.tag}, {self.value}, {self.children}, {self.props}'