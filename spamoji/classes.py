"""
Contains the base construct for Spamoji classes
"""

from typing import TYPE_CHECKING

from spamoji.functions import SpamojiCallable
from spamoji.helpers import SpamojiRuntimeError
from spamoji.token import Token

if TYPE_CHECKING:
    from spamoji.interpreter import Interpreter


class SpamojiClass(SpamojiCallable):
    def __init__(self, name: str) -> None:
        self.name = name

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        instance = SpamojiInstance(self)
        return instance

    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return f"<📜 {self.name}>"


class SpamojiInstance:
    def __init__(self, my_class: SpamojiClass):
        self.my_class = my_class
        self.fields: dict[str, object] = {}

    def get(self, name: Token) -> object:
        if name.lexeme in self.fields:
            return self.fields.get(name.lexeme)
        raise SpamojiRuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def __str__(self) -> str:
        return f"<Instance of {self.my_class}>"
