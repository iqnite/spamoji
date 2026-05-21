"""
Tests for the Parser class.
"""

from pathlib import Path
import unittest

from interpreter import stmt
from interpreter.parser import Parser
from interpreter.scanner import Scanner


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
        self.assertEqual(len(ast), 3)
        self.assertIsInstance(ast[1], stmt.While)
        assert isinstance(ast[1], stmt.While)
        self.assertIsInstance(ast[1].body, stmt.Block)
        assert isinstance(ast[1].body, stmt.Block)
        self.assertEqual(len(ast[1].body.statements), 3)
        self.assertIsInstance(ast[1].body.statements[1], stmt.If)
        self.assertIsInstance(ast[1].body.statements[1], stmt.If)
        assert isinstance(ast[1].body.statements[1], stmt.If)
        self.assertIsInstance(ast[1].body.statements[1].then_branch, stmt.Block)
        self.assertIsInstance(ast[1].body.statements[1].else_branch, stmt.Block)
        self.assertIsInstance(ast[1].body.statements[2], stmt.Expression)
        assert isinstance(ast[1].body.statements[2], stmt.Expression)
        self.assertIsInstance(ast[2], stmt.Expression)


if __name__ == "__main__":
    unittest.main()
