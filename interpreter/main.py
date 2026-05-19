"""
Entry point for the Spamoji interpreter.
"""

import sys

from interpreter.helpers import ASTPrinter, SpamojiRuntimeError
from interpreter.interpreter import Interpreter
from interpreter.parser import Parser
from interpreter.scanner import Scanner


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
            lines = f.readlines()
            for line in lines:
                self.run(line)
        if self.had_error:
            sys.exit(65)
        if self.had_runtime_error:
            sys.exit(70)

    def repl(self):
        """Allows to enter commands and evaluate them interactively."""
        print("🍝 Spamoji REPL v1.0")
        try:
            while True:
                line = input("> ")
                self.run(line)
        except KeyboardInterrupt:
            sys.exit()

    def run(self, source: str):
        """Runs a piece of code."""
        scanner = Scanner(source, self.error)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, self.report)
        expression = parser.parse()
        if expression is None:
            return
        self.interpreter.interpret(expression, self.runtime_error)

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


if __name__ == "__main__":
    Spamoji().main()
