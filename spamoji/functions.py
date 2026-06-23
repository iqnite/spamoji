"""
Contains classes for functions and callables.
"""

import inspect
import typing

from spamoji import stmt
from spamoji.environment import Environment

if typing.TYPE_CHECKING:
    from spamoji.classes import SpamojiInstance
    from spamoji.interpreter import Interpreter


class SpamojiCallable:
    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object: ...
    def arity(self) -> int: ...


class SpamojiFunction(SpamojiCallable):
    def __init__(
        self, declaration: stmt.Function, closure: Environment, is_initializer: bool
    ):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def bind(self, instance: "SpamojiInstance") -> "SpamojiFunction":
        environment = Environment(self.closure)
        environment.define("🤖", instance)
        return SpamojiFunction(self.declaration, environment, self.is_initializer)

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        environment = Environment(self.closure)
        for i, arg in enumerate(self.declaration.arguments):
            environment.define(arg.lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            if self.is_initializer:
                return self.closure.get_at(0, "🤖")
            return return_value.value
        if self.is_initializer:
            return self.closure.get_at(0, "🤖")

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


def spamoji_function(emoji: str | None = None) -> typing.Callable:
    """
    Decorator to mark a function as a Spamoji native function.
    The function will be registered as a native function in the Spamoji interpreter.
    If the emoji parameter is provided, it will be used as the function's emoji name.

    If the function has a parameter named "_interpreter",
    it will be passed the current interpreter instance when called.

    Example usage:
    @spamoji_function("💬")
    def print_function(interpreter, arguments):
        pass
    """

    def decorator(func: typing.Callable) -> typing.Callable:
        parameters = inspect.signature(func).parameters

        def call(interpreter: "Interpreter", arguments: list[object]) -> object:
            if "_interpreter" in parameters:
                interpreter_arg_index = list(parameters).index("_interpreter")
                arguments.insert(interpreter_arg_index, interpreter)
            return func(*arguments)

        spamoji_callable = SpamojiCallable()
        spamoji_callable.call = call
        spamoji_callable.arity = lambda: len(parameters) - int(
            "_interpreter" in parameters
        )
        setattr(func, "_spamoji_emoji", func.__name__ if emoji is None else emoji)
        setattr(func, "_spamoji_callable", spamoji_callable)
        return func

    return decorator
