"""
Contains native functions.
"""

import time
import typing

from interpreter.functions import SpamojiCallable
from interpreter.helpers import SpamojiValueError, spamojiValueError

if typing.TYPE_CHECKING:
    from interpreter.interpreter import Interpreter


class PythonCall(SpamojiCallable):
    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        return eval(str(arguments[0]))

    def arity(self) -> int:
        return 1


class Print(SpamojiCallable):
    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        print(interpreter.stringify(arguments[0]))
        return arguments[0]

    def arity(self) -> int:
        return 1


class PrintNoNewline(Print):
    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        print(interpreter.stringify(arguments[0]), end="")
        return arguments[0]


class GetUserInput(SpamojiCallable):
    def call(self, interpreter: "Interpreter", arguments: list[object]) -> str:
        return input()

    def arity(self) -> int:
        return 0


class ConvertToNumber(SpamojiCallable):
    def call(
        self, interpreter: "Interpreter", arguments: list[object]
    ) -> float | SpamojiValueError:
        try:
            return float(typing.cast(float, arguments[0]))
        except ValueError:
            return spamojiValueError

    def arity(self) -> int:
        return 1


class Clock(SpamojiCallable):
    def call(self, interpreter: "Interpreter", arguments: list[object]) -> float:
        return time.time()

    def arity(self) -> int:
        return 0
