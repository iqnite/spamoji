"""
Contains the base construct for Spamoji classes
"""

from typing import TYPE_CHECKING

from spamoji.functions import SpamojiCallable, SpamojiFunction
from spamoji.helpers import SpamojiRuntimeError
from spamoji.token import Token

if TYPE_CHECKING:
    from spamoji.interpreter import Interpreter


class SpamojiClass(SpamojiCallable):
    def __init__(self, name: str, methods: dict[str, SpamojiFunction]) -> None:
        self.name = name
        self.methods = methods

    def find_method(self, name: str) -> SpamojiFunction | None:
        return self.methods.get(name)

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        instance = SpamojiInstance(self)
        initializer = self.find_method("✨")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def arity(self) -> int:
        initializer = self.find_method("✨")
        if initializer is None:
            return 0
        return initializer.arity()

    def __str__(self) -> str:
        return f"<📜 {self.name}>"


class SpamojiInstance:
    def __init__(self, my_class: SpamojiClass):
        self.my_class = my_class
        self.fields: dict[str, object] = {}

    def get(self, name: Token) -> object:
        if name.lexeme in self.fields:
            return self.fields.get(name.lexeme)
        method = self.my_class.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)
        raise SpamojiRuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name: Token, value: object):
        self.fields[name.lexeme] = value

    def __str__(self) -> str:
        return f"<Instance of {self.my_class}>"
