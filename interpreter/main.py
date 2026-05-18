"""
Entry point for the Spamoji interpreter.
"""

from enum import Enum
import sys


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
    for token in tokens:
        print(token)


class Scanner:
    """Scanner for the Spamoji language."""

    def __init__(self, source: str):
        """
        Initializes a scanner instance.

        :param str source: Source code to scan
        """

    def scan_tokens(self) -> list[Token]:
        """
        Scans the tokens in the given source.

        :returns list[Token]: The tokens contained in the source
        """


class TokenType(Enum):
    LEFT_PAREN = 0
    RIGHT_PAREN = 1
    OPERATOR = 2
    IDENTIFIER = 3
    STRING = 4
    NUMBER = 5
    COMMENT = 6
    FUNCTION = 7
    WHILE = 8
    BREAK = 9
    CONTINUE = 10
    RETURN = 11
    EQUALS = 12
    NOT_EQUALS = 13
    GREATER_THAN = 14
    LESS_THAN = 15
    IF = 16
    IFTRUE = 17
    ELSE = 18
    TRUE = 19
    FALSE = 20
    VAR = 21
    LABEL = 22
    JUMP = 23
    IMPORT = 33
    PYTHON = 34
    AND = 35
    OR = 36
    NOT = 37
    PLUS = 38
    MINUS = 39
    MULTIPLY = 40
    DIVIDE = 41
    SPACE = 42


class Token:
    """Represents a token."""
    
    def __init__(self, token_type):...


def error(line: int, message: str):
    report(line, "", message)

def report(line: int, where: str, message: str):
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)


if __name__ == "__main__":
    main()
