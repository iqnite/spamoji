"""
Contains classes for functions and callables.
"""

from typing import TYPE_CHECKING

from spamoji import stmt
from spamoji.environment import Environment

if TYPE_CHECKING:
    from spamoji.interpreter import Interpreter


class SpamojiCallable:
    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object: ...
    def arity(self) -> int: ...


class SpamojiFunction(SpamojiCallable):
    def __init__(self, declaration: stmt.Function, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        environment = Environment(self.closure)
        for i, arg in enumerate(self.declaration.arguments):
            environment.define(arg.lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            return return_value.value

    def arity(self) -> int:
        return len(self.declaration.arguments)

    def __str__(self) -> str:
        return f"<⚙️ {self.declaration.name.lexeme}>"


class Return(RuntimeError):
    def __init__(self, value: object, *_):
        super().__init__()
        self.value = value


class BreakLoop(RuntimeError):
    pass


class ContinueLoop(RuntimeError):
    pass
