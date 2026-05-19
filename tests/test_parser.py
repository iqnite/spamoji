"""
Tests for the Parser class.
"""

import unittest
import typing

from interpreter.helpers import ASTPrinter
from interpreter.expr import Expr
from interpreter.parser import Parser
from interpreter.scanner import Scanner


class TestParser(unittest.TestCase):
    """Tests for implicit string concatenation parsing."""

    def test_string_concatenates_value_on_both_sides(self):
        source = '1"hi"2'
        tokens = Scanner(source).scan_tokens()
        expr = Parser(tokens).parse()

        self.assertIsNotNone(expr)
        expr = typing.cast(Expr, expr)
        self.assertEqual(ASTPrinter().print(expr), "(➕ (➕ 1.0 hi) 2.0)")


if __name__ == "__main__":
    unittest.main()
