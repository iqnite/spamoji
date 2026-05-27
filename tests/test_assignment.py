"""
Tests for compound assignment evaluation.
"""

import unittest

from spamoji.spamoji import Spamoji
from spamoji.token import Token, TokenType


class TestCompoundAssignment(unittest.TestCase):
    """Compound assignment regression tests."""

    def test_variable_compound_assignment_updates_value(self):
        source = "👋 x 🫴 10\nx 🫴➕ 5\nx 🫴➖ 2\nx 🫴✖️ 3\nx 🫴➗ 13\n"

        app = Spamoji()
        app.run(source)

        self.assertFalse(app.had_error)
        self.assertFalse(app.had_runtime_error)

        value = app.interpreter.globals.get(Token(TokenType.IDENTIFIER, "x", "x", 1))

        self.assertEqual(value, 3.0)


if __name__ == "__main__":
    unittest.main()
