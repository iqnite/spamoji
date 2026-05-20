"""
Tests for the Scanner class.
"""

import unittest

from interpreter.scanner import Scanner
from interpreter.token import TokenType


class TestScanner(unittest.TestCase):
    """Tests for indentation scanning."""

    def test_indented_line_emits_indent_token(self):
        source = "👋 x 1\n    🐍 🔤print(x)🔤\n"
        tokens = Scanner(source).scan_tokens()

        token_types = [token.token_type for token in tokens]

        self.assertIn(TokenType.INDENT, token_types)


if __name__ == "__main__":
    unittest.main()
