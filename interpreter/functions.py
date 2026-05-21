"""
Contains classes for functions and callables.
"""

from typing import TYPE_CHECKING

from interpreter import stmt
from interpreter.environment import Environment

if TYPE_CHECKING:
    from interpreter.interpreter import Interpreter


class SpamojiCallable:
    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object: ...
    def arity(self) -> int: ...


class SpamojiFunction(SpamojiCallable):
    def __init__(self, declaration: stmt.Function):
        self.declaration = declaration

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        environment = Environment(interpreter.globals)
        for arg in self.declaration.arguments:
            environment.define(arg.lexeme, arg)
        interpreter.execute_block(self.declaration.body, environment)

    def arity(self) -> int:
        return len(self.declaration.arguments)

    def __str__(self) -> str:
        return f"<⚙️ {self.declaration.name.lexeme}>"
