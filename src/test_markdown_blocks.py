import unittest
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type
class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = "Block 1\n\n\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

class TestBlockToBlockType(unittest.TestCase):

    def test_heading_types(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Mid Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Tiny Heading"), BlockType.HEADING)

        self.assertEqual(block_to_block_type("####### Too Many"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)


    def test_code_block(self):
        code = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
        invalid_code = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(invalid_code), BlockType.PARAGRAPH)

    def test_quote_block(self):
        quote = "> This is a quote\n> with multiple lines" 
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        invalid_quote = "> Line 1\nLine 2"
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.PARAGRAPH) 

    def test_unordered_list(self):
        ul = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)
        invalid_ul = "-Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(invalid_ul), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        ol = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)
        bad_start = "2. Second\n3. Third"
        self.assertEqual(block_to_block_type(bad_start), BlockType.PARAGRAPH)
        broken_seq = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(broken_seq), BlockType.PARAGRAPH)

    def test_paragraph(self):
        para = "This is just a normal paragraph of text." 
        self.assertEqual(block_to_block_type(para), BlockType.PARAGRAPH)   
     

if __name__ == "__main__":
    unittest.main()       
