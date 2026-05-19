"""
Contains classes and functions for variable environments.
"""

from interpreter.helpers import SpamojiRuntimeError
from interpreter.token import Token


class Environment:
    values: dict[str, object]

    def __init__(self):
        self.values = {}

    def define(self, name: str, value: object):
        self.values[name] = value

    def assign(self, token: Token, value: object):
        self.values[token.lexeme] = value

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise SpamojiRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
