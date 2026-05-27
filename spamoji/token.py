"""
This module defines the Token class and the TokenType enumeration for the Spamoji programming language.
"""

from enum import Enum


class TokenType(Enum):
    LEFT_PAREN = 0
    RIGHT_PAREN = 1
    IDENTIFIER = 3
    STRING = 4
    NUMBER = 5
    FUNCTION = 7
    WHILE = 8
    BREAK = 9
    CONTINUE = 10
    RETURN = 11
    EQUALS = 12
    NOT_EQUALS = 13
    GREATER_THAN = 14
    GREATER_THAN_OR_EQUAL = 56
    LESS_THAN_OR_EQUAL = 57
    LESS_THAN = 15
    IF = 16
    IFTRUE = 17
    ELSE = 18
    TRUE = 19
    FALSE = 20
    VAR = 21
    # IMPORT = 33
    OR = 36
    NOT = 37
    PLUS = 38
    MINUS = 39
    MULTIPLY = 40
    DIVIDE = 41
    EOF = 44
    NULL = 45
    NEWLINE = 46
    AND = 47
    INDENT = 48
    ASSIGNMENT = 49
    PLUS_ASSIGNMENT = 50
    COMMA = 51
    CLASS = 52
    DOT = 53
    THIS = 54
    SUPER = 55
    MINUS_ASSIGNMENT = 58
    MULTIPLY_ASSIGNMENT = 59
    DIVIDE_ASSIGNMENT = 60


class Token:
    """Represents a token."""

    def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int):
        """
        Initializes a token instance.

        :param TokenType token_type: The type of the token
        :param str lexeme: The actual text of the token
        :param object literal: The literal value of the token, if applicable
        :param int line: The line number where the token was found
        """
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f"{self.token_type} {self.lexeme} {self.literal}"
