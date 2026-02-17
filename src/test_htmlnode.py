import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com"',
        )

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        result = node.props_to_html()
        self.assertIn(' href="https://www.google.com"', result)
        self.assertIn(' target="_blank"', result)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")    

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "my template text", {"href": "www.thetemplatelink.com"})    
        self.assertEqual(
            node.to_html(),
            '<a href="www.thetemplatelink.com">my template text</a>',
        )

    def test_parent_simple(self):
        node = ParentNode("div", [LeafNode("span", "child")])
        self.assertEqual(node.to_html(), "<div><span>child</span></div>")
    
if __name__ == "__main__":
    unittest.main()
            
