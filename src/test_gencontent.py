import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_standard_h1(self):
        # Basic case: single # followed by space
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extra_whitespace(self):
        # Should strip leading/trailing whitespace from the title text
        self.assertEqual(extract_title("#   Title with Spaces   "), "Title with Spaces")

    def test_h1_with_subtitle(self):
        # Should ignore H2 (##) and correctly find the single # H1
        md = "## Subtitle\n# Main Title\n### Small Header"
        self.assertEqual(extract_title(md), "Main Title")

    def test_no_h1_raises_exception(self):
        # Should raise an exception when no line starts with exactly one #
        md = "## Just a subtitle\nNo header here"
        with self.assertRaises(Exception) as cm:
            extract_title(md)
        self.assertEqual(str(cm.exception), "No H1 header found")

    def test_h1_not_at_start(self):
        # Should find H1 even if it's not the first line of the file
        md = "Some introductory text.\n\n# The Actual Title"
        self.assertEqual(extract_title(md), "The Actual Title")

    def test_multiple_hashes_ignored(self):
        # Ensure '###' is not mistaken for '#'
        md = "### Header 3\n# Header 1"
        self.assertEqual(extract_title(md), "Header 1")

if __name__ == "__main__":
    unittest.main()
