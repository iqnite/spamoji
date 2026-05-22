"""
Entry point for the Spamoji interpreter.
"""

import sys

from spamoji.helpers import SpamojiRuntimeError
from spamoji.interpreter import Interpreter
from spamoji.parser import Parser
from spamoji.scanner import Scanner


class Spamoji:
    def __init__(self):
        self.interpreter = Interpreter()
        self.had_error = False
        self.had_runtime_error = False

    def main(self):
        """Main entry point.
        Gets a script file name from the command arguments, or launches the REPL."""
        if len(sys.argv) == 1:
            self.repl()
        else:
            self.run_file(sys.argv[1])

    def run_file(self, filename):
        """Runs a script file."""
        with open(filename, "r", encoding="utf-8") as f:
            self.run(f.read())
        if self.had_error:
            sys.exit(65)
        if self.had_runtime_error:
            sys.exit(70)

    def repl(self):
        """Allows to enter commands and evaluate them interactively."""
        print("🍝 Spamoji REPL v0.1.0")
        print(
            "Visit https://github.com/iqnite/spamoji#readme-ov-file for help. Press Ctrl+C to exit."
        )
        try:
            while True:
                line = input("> ") + "\n"
                self.run(line, print_expressions=True)
        except KeyboardInterrupt:
            sys.exit()

    def run(self, source: str, print_expressions: bool = False):
        """Runs a piece of code."""
        scanner = Scanner(source, self.error)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, self.report)
        statements = parser.parse()
        if self.had_error:
            return
        self.interpreter.interpret(
            statements,
            print_expressions=print_expressions,
            error_handler=self.runtime_error,
        )

    def error(self, line: int, message: str):
        """Reports an error with a given message and line number."""
        self.report(line, "", message)

    def runtime_error(self, error: SpamojiRuntimeError):
        print(f"{error}\n[line {error.token.line}]")
        self.had_runtime_error = True

    def report(self, line: int, where: str, message: str):
        """Reports an error with a given message and line number."""
        self.had_error = True
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)


def main():
    Spamoji().main()


if __name__ == "__main__":
    main()
