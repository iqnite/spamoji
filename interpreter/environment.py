"""
Contains classes and functions for variable environments.
"""

from interpreter.helpers import SpamojiRuntimeError
from interpreter.token import Token


class Environment:
    values: dict[str, object]
    enclosing: "Environment | None"

    def __init__(self, enclosing: "Environment | None" = None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name: str, value: object):
        self.values[name] = value

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise SpamojiRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise SpamojiRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
