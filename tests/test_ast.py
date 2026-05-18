"""
Test functions for the Spamoji interpreter.
"""

import unittest
from interpreter.expr import Binary, Expr, Grouping, Literal, Unary, Visitor
from interpreter.helpers import ASTPrinter
from interpreter.token import Token, TokenType


class TestASTPrinter(unittest.TestCase):
    """Tests the ASTPrinter class."""

    def test_ast_printer(self):
        """Tests the ASTPrinter class."""
        printer = ASTPrinter()
        expr = Binary(
            left=Unary(
                operator=Token(
                    token_type=TokenType.MINUS, lexeme="➖", literal=None, line=1
                ),
                right=Literal(value=123),
            ),
            operator=Token(
                token_type=TokenType.MULTIPLY, lexeme="✖️", literal=None, line=1
            ),
            right=Grouping(expression=Literal(value=45.67)),
        )
        self.assertEqual(printer.print(expr), "(✖️ (➖ 123) (group 45.67))")


if __name__ == "__main__":
    unittest.main()
