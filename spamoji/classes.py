"""
Contains the base construct for Spamoji classes
"""

from typing import TYPE_CHECKING

from spamoji.functions import SpamojiCallable

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


class SpamojiInstance:
    def __init__(self, my_class: SpamojiClass):
        self.my_class = my_class
