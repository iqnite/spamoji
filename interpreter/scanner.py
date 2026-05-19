"""
This module contains the Scanner class for the Spamoji programming language.
"""

import typing

from interpreter.token import Token, TokenType


class Scanner:
    """Scanner for the Spamoji language."""

    def __init__(
        self,
        source: str,
        error_handler: typing.Callable[[int, str], typing.Any] | None = None,
    ):
        """
        Initializes a scanner instance.

        :param str source: Source code to scan
        """
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.error_handler = error_handler

    def scan_tokens(self) -> list[Token]:
        """
        Scans the tokens in the given source.

        :returns list[Token]: The tokens contained in the source
        """
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
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
                self.add_token(TokenType.NEWLINE)
                self.line += 1
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "🗒️":
                self.add_token(TokenType.COMMENT)
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
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
            if self.error_handler:
                self.error_handler(self.line, "Unterminated string.")
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
        if text in KEYWORDS:
            self.add_token(KEYWORDS[text])
            return

        self.add_token(TokenType.IDENTIFIER, text)


KEYWORDS = {
    "⚙️": TokenType.FUNCTION,
    "🔃": TokenType.WHILE,
    "⛔": TokenType.BREAK,
    "⤴️": TokenType.CONTINUE,
    "↪️": TokenType.RETURN,
    "🟰": TokenType.EQUALS,
    "🆚": TokenType.NOT_EQUALS,
    "🤜": TokenType.GREATER_THAN,
    "🤛": TokenType.LESS_THAN,
    "🤔": TokenType.IF,
    "👍": TokenType.IFTRUE,
    "👎": TokenType.ELSE,
    "✅": TokenType.TRUE,
    "❌": TokenType.FALSE,
    "👋": TokenType.VAR,
    "🚩": TokenType.LABEL,
    "🎯": TokenType.JUMP,
    "🧩": TokenType.IMPORT,
    "🐍": TokenType.PYTHON,
    "🤝": TokenType.AND,
    "🤲": TokenType.OR,
    "🙅": TokenType.NOT,
    "➕": TokenType.PLUS,
    "➖": TokenType.MINUS,
    "✖️": TokenType.MULTIPLY,
    "➗": TokenType.DIVIDE,
    "🛑": TokenType.STOP,
    "⚠️": TokenType.ERROR,
}
