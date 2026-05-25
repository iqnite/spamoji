"""
Tests for import module behavior.
"""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from spamoji.spamoji import Spamoji
from spamoji.token import Token, TokenType


class TestImports(unittest.TestCase):
    """Import regression tests."""

    def test_imported_module_symbols_are_accessible_by_module_name(self):
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            imported_file = temp_path / "lib.🍝"
            main_file = temp_path / "main.🍝"

            imported_file.write_text("👋 x 🫴 1\n", encoding="utf-8")
            main_file.write_text("🧩 lib.🍝\n👋 x 🫴 2\n", encoding="utf-8")

            app = Spamoji()
            app.run(main_file.read_text(encoding="utf-8"), filename=str(main_file))

            self.assertFalse(app.had_error)
            self.assertFalse(app.had_runtime_error)

            module_name = Token(TokenType.IDENTIFIER, "lib", "lib", 1)
            imported_module = app.interpreter.globals.get(module_name)
            imported_symbol = imported_module.get(
                Token(TokenType.IDENTIFIER, "x", "x", 1)
            )

            self.assertEqual(imported_symbol, 1.0)


if __name__ == "__main__":
    unittest.main()
