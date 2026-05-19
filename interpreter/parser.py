"""
Parser for the Spamoji language. Converts a list of tokens into an abstract syntax tree (AST).
"""

import typing

from interpreter.expr import Binary, Expr, Grouping, Literal, Unary
from interpreter.helpers import error_token
from interpreter.token import Token, TokenType


class ParseError(Exception):
    """Exception class for parse errors."""

    pass


class Parser:
    """Parser for the Spamoji language. Converts a list of tokens into an AST."""

    def __init__(
        self,
        tokens: list[Token],
        error_handler: typing.Callable[[int, str, str], typing.Any] | None = None,
    ):
        """
        Initializes the parser with a list of tokens.
        :param list[Token] tokens: The list of tokens to parse.
        """
        self.tokens = tokens
        self.current = 0
        self.error_handler = error_handler

    def parse(self) -> Expr | None:
        """Parses the tokens and returns the resulting AST."""
        try:
            return self.expression()
        except ParseError:
            return None

    def expression(self) -> Expr:
        """Parses an expression."""
        return self.logic_or()

    def equality(self) -> Expr:
        """Parses an equality expression."""
        expr = self.comparison()
        while self.match(TokenType.NOT_EQUALS, TokenType.EQUALS):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def match(self, *types: TokenType) -> bool:
        """Checks if the current token matches any of the given types."""
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
        """Checks if the current token is of the given type."""
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type

    def advance(self) -> Token:
        """Advances to the next token and returns the previous one."""
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        """Checks if we've reached the end of the token list."""
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token:
        """Returns the current token without advancing."""
        return self.tokens[self.current]

    def previous(self) -> Token:
        """Returns the most recently consumed token."""
        return self.tokens[self.current - 1]

    def logic_or(self) -> Expr:
        expr = self.logic_and()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.logic_and()
            expr = Binary(expr, operator, right)
        return expr

    def logic_and(self) -> Expr:
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(TokenType.GREATER_THAN, TokenType.LESS_THAN):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.MINUS, TokenType.NOT):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NULL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        raise self.error(self.peek(), "Expected expression.")

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str) -> ParseError:
        if self.error_handler:
            error_token(token, message, self.error_handler)
        return ParseError()

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().token_type == TokenType.NEWLINE:
                return
            if self.peek().token_type in (
                TokenType.FUNCTION,
                TokenType.VAR,
                TokenType.LABEL,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.RETURN,
            ):
                return
            self.advance()
