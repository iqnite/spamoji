"""
Tests for example scripts.
"""

import io
import unittest
from unittest.mock import patch

from spamoji.spamoji import Spamoji


class TestExamples(unittest.TestCase):
    """Example tests."""

    def setUp(self):
        super().setUp()
        self.app = Spamoji()

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["Bob", "3.1", "10"])
    def test_factorial_example(self, mock_input: io.StringIO, mock_stdout: io.StringIO):
        self.app.run_file("examples/factorial.🍝")
        self.assertFalse(self.app.had_error)
        self.assertFalse(self.app.had_runtime_error)
        self.assertEqual(
            mock_stdout.getvalue(),
            "Enter a number to calculate the factorial: Invalid input. Please enter a number.\nEnter a number to calculate the factorial: Cannot calculate for floating point numbers. Please enter an integer.\nEnter a number to calculate the factorial: The factorial of 10 is 3628800\nThat's a very large number!\n",
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["test", "stop"])
    def test_flowcontrol_example(
        self, mock_input: io.StringIO, mock_stdout: io.StringIO
    ):
        self.app.run_file("examples/flowcontrol.🍝")
        self.assertFalse(self.app.had_error)
        self.assertFalse(self.app.had_runtime_error)
        self.assertEqual(
            mock_stdout.getvalue(),
            '1 <= 5 -> continue\n2 <= 5 -> continue\n3 <= 5 -> continue\n4 <= 5 -> continue\n5 <= 5 -> continue\n6 > 5 -> no continue\n7 > 5 -> no continue\n8 > 5 -> no continue\n9 > 5 -> no continue\n10 > 5 -> no continue\n11 > 10 -> finishing\n12 > 10 -> finishing\n13 > 10 -> finishing\n14 > 10 -> finishing\nFinished, type "stop" to stop\nStopped\n',
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_highorder_example(self, mock_stdout: io.StringIO):
        self.app.run_file("examples/highorder.🍝")
        self.assertFalse(self.app.had_error)
        self.assertFalse(self.app.had_runtime_error)
        self.assertIn(mock_stdout.getvalue(), ["Hello!\n", "Goodbye!\n"])

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_implicit_call_example(self, mock_stdout: io.StringIO):
        self.app.run_file("examples/implicit_call.🍝")
        self.assertFalse(self.app.had_error)
        self.assertFalse(self.app.had_runtime_error)
        self.assertEqual(
            mock_stdout.getvalue(),
            "Beep boop! I am Clanker!\nHello Clanker! I am 💀 Terminator!\nPEW PEW PEW \nCannot shoot more than 100 times!\n",
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_imports_example(self, mock_stdout: io.StringIO):
        self.app.run_file("examples/imports.🍝")
        self.assertFalse(self.app.had_error)
        self.assertFalse(self.app.had_runtime_error)
        self.assertEqual(
            mock_stdout.getvalue(),
            "Beep boop! I am Clanker!\nHello Clanker! I am 💀 Terminator!\nPEW PEW PEW \nCannot shoot more than 100 times!\n",
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["5"])
    def test_random_example(self, mock_input: io.StringIO, mock_stdout: io.StringIO):
        self.app.run_file("examples/random.🍝")
        self.assertFalse(self.app.had_error)
        self.assertFalse(self.app.had_runtime_error)
        self.assertIn(
            mock_stdout.getvalue()[0],
            "012345",
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_recursion_example(self, mock_stdout: io.StringIO):
        self.app.run_file("examples/recursion.🍝")
        self.assertFalse(self.app.had_error)
        self.assertFalse(self.app.had_runtime_error)
        self.assertEqual(
            mock_stdout.getvalue(),
            "0\n1\n1\n2\n3\n5\n8\n13\n21\n34\n55\n89\n144\n233\n377\n610\n987\n1597\n2584\n4181\n",
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_sine_example(self, mock_stdout: io.StringIO):
        self.app.run_file("examples/sine.🍝")
        self.assertFalse(self.app.had_error)
        self.assertFalse(self.app.had_runtime_error)
        self.assertEqual(
            mock_stdout.getvalue(), "The sine of 3 is: 0.1411200080598672\n"
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_strings_example(self, mock_stdout: io.StringIO):
        self.app.run_file("examples/strings.🍝")
        self.assertFalse(self.app.had_error)
        self.assertFalse(self.app.had_runtime_error)
        self.assertEqual(
            mock_stdout.getvalue(),
            "Use the 🔤 character around strings, use the 🚧 character to escape values!\n",
        )


if __name__ == "__main__":
    unittest.main()
