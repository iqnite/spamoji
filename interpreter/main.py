"""
Entry point for the Spamoji interpreter.
"""

import sys

from interpreter.token import Token, TokenType


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
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> list[Token]:
        """
        Scans the tokens in the given source.

        :returns list[Token]: The tokens contained in the source
        """
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        return self.tokens

    def is_at_end(self) -> bool:
        """Checks if the scanner has reached the end of the source."""
        return self.current >= len(self.source)

    def scan_token(self):
        """Scans a single token."""
        c = self.advance()
        match c:
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "🗒️":
                self.add_token(TokenType.COMMENT)
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            case "⚙️":
                self.add_token(TokenType.FUNCTION)
            case "🔃":
                self.add_token(TokenType.WHILE)
            case "⛔":
                self.add_token(TokenType.BREAK)
            case "⤴️":
                self.add_token(TokenType.CONTINUE)
            case "↪️":
                self.add_token(TokenType.RETURN)
            case "🟰":
                self.add_token(TokenType.EQUALS)
            case "🆚":
                self.add_token(TokenType.NOT_EQUALS)
            case "🤜":
                self.add_token(TokenType.GREATER_THAN)
            case "🤛":
                self.add_token(TokenType.LESS_THAN)
            case "🤔":
                self.add_token(TokenType.IF)
            case "👍":
                self.add_token(TokenType.IFTRUE)
            case "👎":
                self.add_token(TokenType.ELSE)
            case "✅":
                self.add_token(TokenType.TRUE)
            case "❌":
                self.add_token(TokenType.FALSE)
            case "👋":
                self.add_token(TokenType.VAR)
            case "🚩":
                self.add_token(TokenType.LABEL)
            case "🎯":
                self.add_token(TokenType.JUMP)
            case "🧩":
                self.add_token(TokenType.IMPORT)
            case "🐍":
                self.add_token(TokenType.PYTHON)
            case "🤝":
                self.add_token(TokenType.OR)
            case "🙅":
                self.add_token(TokenType.NOT)
            case "➕":
                self.add_token(TokenType.PLUS)
            case "➖":
                self.add_token(TokenType.MINUS)
            case "✖️":
                self.add_token(TokenType.MULTIPLY)
            case "➗":
                self.add_token(TokenType.DIVIDE)
            case "🛑":
                self.add_token(TokenType.STOP)
            case "⚠️":
                self.add_token(TokenType.ERROR)
            case '"':
                self.string()
            case _:
                if c.isdigit():
                    self.number()
                else:
                    self.identifier()

    def advance(self) -> str:
        """Advances the scanner and returns the next character."""
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type: TokenType, literal: object = None):
        """Adds a token to the list of tokens."""
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        """Checks if the next character matches the expected character."""
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        """Returns the next character without advancing the scanner."""
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def string(self):
        """Scans a string literal."""
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            error(self.line, "Unterminated string.")
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        """Scans a number literal."""
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            # Consume the "."
            self.advance()

            while self.peek().isdigit():
                self.advance()

        value = float(self.source[self.start : self.current])
        self.add_token(TokenType.NUMBER, value)

    def peek_next(self) -> str:
        """Returns the character after the next character without advancing the scanner."""
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def identifier(self):
        """Scans an identifier."""
        while self.peek() not in ' \r\t\n()".,;' and not self.is_at_end():
            self.advance()

        text = self.source[self.start : self.current]
        self.add_token(TokenType.IDENTIFIER, text)


def error(line: int, message: str):
    report(line, "", message)


def report(line: int, where: str, message: str):
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)


if __name__ == "__main__":
    main()
