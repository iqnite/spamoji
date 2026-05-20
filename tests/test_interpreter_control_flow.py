"""Tests for interpreter loop control flow (break/continue)."""

import unittest

from interpreter.interpreter import Interpreter
from interpreter.parser import Parser
from interpreter.scanner import Scanner


def run_source(source: str) -> Interpreter:
    interpreter = Interpreter()
    tokens = Scanner(source).scan_tokens()
    statements = Parser(tokens).parse()
    interpreter.interpret(statements)
    return interpreter


class TestInterpreterControlFlow(unittest.TestCase):
    def test_break_skips_remaining_body_statements(self):
        source = """👋 i 🫴 0
👋 x 🫴 0
🔃 i 🤛 3
    i 🫴 i ➕ 1
    ⛔
    x 🫴 x ➕ 1
"""

        interpreter = run_source(source)

        self.assertEqual(interpreter.environment.values["i"], 1.0)
        self.assertEqual(interpreter.environment.values["x"], 0.0)

    def test_continue_skips_remaining_body_statements(self):
        source = """👋 i 🫴 0
👋 x 🫴 0
🔃 i 🤛 3
    i 🫴 i ➕ 1
    ⤴️
    x 🫴 x ➕ 1
"""

        interpreter = run_source(source)

        self.assertEqual(interpreter.environment.values["i"], 3.0)
        self.assertEqual(interpreter.environment.values["x"], 0.0)

    def test_break_level_propagates_out_of_nested_loops(self):
        source = """👋 i 🫴 0
🔃 i 🤛 3
    i 🫴 i ➕ 1
    👋 j 🫴 0
    🔃 j 🤛 3
        j 🫴 j ➕ 1
        ⛔ 2
"""

        interpreter = run_source(source)

        self.assertEqual(interpreter.environment.values["i"], 1.0)


if __name__ == "__main__":
    unittest.main()
