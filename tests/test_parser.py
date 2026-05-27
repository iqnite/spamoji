"""
Tests for the Parser class.
"""

from pathlib import Path
import unittest

from spamoji import expr
from spamoji import stmt
from spamoji.parser import Parser
from spamoji.scanner import Scanner
from spamoji.token import TokenType


class TestParser(unittest.TestCase):
    """Parser regression tests."""

    def test_nested_flow_control_example_parses(self):
        source = Path("examples/flowcontrol.🍝").read_text(encoding="utf-8")
        tokens = Scanner(source).scan_tokens()

        errors: list[tuple[int, str, str]] = []

        def error_handler(line: int, token_info: str, message: str):
            errors.append((line, token_info, message))

        ast = Parser(tokens, error_handler).parse()

        self.assertEqual(errors, [])
        self.assertEqual(len(ast), 5)
        self.assertIsInstance(ast[1], stmt.While)
        assert isinstance(ast[1], stmt.While)
        self.assertIsNotNone(ast[1].body)
        self.assertIsInstance(ast[1].body, stmt.Block)
        assert isinstance(ast[1].body, stmt.Block)
        self.assertGreaterEqual(len(ast[1].body.statements), 2)
        self.assertIsInstance(ast[1].body.statements[1], stmt.If)
        assert isinstance(ast[1].body.statements[1], stmt.If)
        self.assertIsInstance(ast[1].body.statements[1].then_branch, stmt.Block)
        if ast[1].body.statements[1].else_branch is not None:
            self.assertIsInstance(ast[1].body.statements[1].else_branch, stmt.Block)
        if len(ast[1].body.statements) > 2:
            self.assertIsInstance(ast[1].body.statements[2], stmt.Expression)
            assert isinstance(ast[1].body.statements[2], stmt.Expression)
        self.assertIsInstance(ast[2], stmt.Expression)

    def test_string_followed_by_parenthesized_expression_concatenates(self):
        source = "🔤hello🔤🫸1🫷\n"
        tokens = Scanner(source).scan_tokens()

        ast = Parser(tokens).parse()

        self.assertEqual(len(ast), 1)
        self.assertIsInstance(ast[0], stmt.Expression)
        assert isinstance(ast[0], stmt.Expression)
        self.assertIsInstance(ast[0].expression, expr.Binary)
        assert isinstance(ast[0].expression, expr.Binary)
        self.assertIsInstance(ast[0].expression.left, expr.Literal)
        self.assertIsInstance(ast[0].expression.right, expr.Grouping)

    def test_compound_assignment_parses_with_operator(self):
        source = "x 🫴➕ 1\n"
        tokens = Scanner(source).scan_tokens()

        ast = Parser(tokens).parse()

        self.assertEqual(len(ast), 1)
        self.assertIsInstance(ast[0], stmt.Expression)
        assert isinstance(ast[0], stmt.Expression)
        self.assertIsInstance(ast[0].expression, expr.Assign)
        assert isinstance(ast[0].expression, expr.Assign)
        self.assertEqual(ast[0].expression.name.lexeme, "x")
        self.assertIsNotNone(ast[0].expression.operator)
        assert ast[0].expression.operator is not None
        self.assertEqual(ast[0].expression.operator.token_type, TokenType.PLUS)

        self.assertIsInstance(ast[0].expression.value, expr.Literal)


if __name__ == "__main__":
    unittest.main()
