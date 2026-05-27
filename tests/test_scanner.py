"""
Tests for the Scanner class.
"""

import unittest

from spamoji.scanner import Scanner
from spamoji.token import TokenType


class TestScanner(unittest.TestCase):
    """Tests for indentation scanning."""

    def test_indented_line_emits_indent_token(self):
        source = "👋 x 1\n    🐍 🔤print(x)🔤\n"
        tokens = Scanner(source).scan_tokens()

        token_types = [token.token_type for token in tokens]

        self.assertIn(TokenType.INDENT, token_types)

    def test_compound_assignment_tokens_are_scanned(self):
        source = "👋 x 🫴➕ 1\n👋 y 🫴➖ 2\n👋 z 🫴✖️ 3\n👋 w 🫴➗ 4\n"
        tokens = Scanner(source).scan_tokens()

        token_types = [token.token_type for token in tokens]

        self.assertIn(TokenType.PLUS_ASSIGNMENT, token_types)
        self.assertIn(TokenType.MINUS_ASSIGNMENT, token_types)
        self.assertIn(TokenType.MULTIPLY_ASSIGNMENT, token_types)
        self.assertIn(TokenType.DIVIDE_ASSIGNMENT, token_types)


if __name__ == "__main__":
    unittest.main()
