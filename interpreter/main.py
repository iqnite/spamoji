"""
Entry point for the Spamoji interpreter.
"""

import sys

from interpreter.helpers import ASTPrinter
from interpreter.parser import Parser
from interpreter.scanner import Scanner


def main():
    """Main entry point.
    Gets a script file name from the command arguments, or launches the REPL."""
    if len(sys.argv) == 1:
        repl()
    else:
        run_file(sys.argv[1])


def run_file(filename):
    """Runs a script file."""
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            run(line)


def repl():
    """Allows to enter commands and evaluate them interactively."""
    print("🍝 Spamoji REPL v1.0")
    try:
        while True:
            line = input("> ")
            run(line)
    except KeyboardInterrupt:
        sys.exit()


def run(source: str):
    """Runs a piece of code."""
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    expression = parser.parse()
    if expression is None:
        return
    print(ASTPrinter().print(expression))


if __name__ == "__main__":
    main()
