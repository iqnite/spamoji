"""
Contains helper functions and classes for the Spamoji interpreter.
"""

import sys

from interpreter.expr import Binary, Expr, Grouping, Literal, Unary, Visitor
from interpreter.token import Token, TokenType


def report(line: int, where: str, message: str):
    """Reports an error with a given message and line number."""
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)


def error(line: int, message: str):
    """Reports an error with a given message and line number."""
    report(line, "", message)


def error_token(token: Token, message: str):
    """Reports an error with a given message and token."""
    if token.token_type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)


class ASTPrinter(Visitor):
    """Prints an AST in a human-readable format."""

    def print(self, expr: Expr) -> str:
        """Prints an AST in a human-readable format."""
        return f"{expr.accept(self)}"

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        result = f"({name}"
        for expr in exprs:
            result += f" {expr.accept(self)}"
        result += ")"
        return result


class SpamojiRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str, *args: object):
        super().__init__(message, *args)
        self.token = token


def runtime_error(error: SpamojiRuntimeError):
    print(f"{error}\n[line {error.token.line}]")
