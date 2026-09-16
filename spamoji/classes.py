"""
Contains the base construct for Spamoji classes
"""

import inspect
from typing import TYPE_CHECKING
import typing

from spamoji.environment import Environment
from spamoji.expr import Expr
from spamoji.functions import SpamojiCallable, SpamojiFunction, spamoji_function
from spamoji.helpers import SpamojiRuntimeError
from spamoji.token import Token

if TYPE_CHECKING:
    from spamoji.interpreter import Interpreter


class SpamojiClass(SpamojiCallable):
    def __init__(
        self,
        name: str,
        superclasses: list["SpamojiClass"],
        methods: dict[str, SpamojiFunction],
    ) -> None:
        self.name = name
        self.superclasses = superclasses
        self.methods = methods

    def find_method(self, name: str) -> SpamojiFunction | None:
        if name in self.methods:
            return self.methods.get(name)
        for superclass in self.superclasses:
            method = superclass.find_method(name)
            if method is not None:
                return method

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


class SpamojiModule:
    def __init__(
        self,
        name: str,
        environment: Environment,
        locals: dict[Expr, int] | None = None,
    ):
        self.name = name
        self.environment = environment
        self.locals: dict[Expr, int] = locals or {}

    def get(self, name: Token) -> object:
        return self.environment.get(name)

    def set(self, name: Token, value: object):
        try:
            self.environment.assign(name, value)
        except SpamojiRuntimeError:
            self.environment.define(name.lexeme, value)

    def __str__(self) -> str:
        return f"<🧩 {self.name}>"


def spamoji_class(emoji: str | None = None) -> typing.Callable:
    """
    Decorator to mark a class as a Spamoji native class.
    The class will be registered as a native class in the Spamoji interpreter.
    If the emoji parameter is provided, it will be used as the class's emoji name.

    Example usage:
    @spamoji_class("🎁")
    class MyNativeClass:
        pass
    """

    def decorator(cls: typing.Type) -> typing.Callable:
        if hasattr(cls, "_spamoji_class"):
            return cls

        class WrappedClass(cls, SpamojiClass):
            def __init__(self, *args, **kwargs):
                cls.__init__(self, *args, **kwargs)
                SpamojiClass.__init__(
                    self,
                    name=emoji or cls.__name__,
                    superclasses=[
                        spamoji_class()(superclass)
                        for superclass in cls.__bases__
                        if superclass is not object
                    ],
                    methods={
                        name: SpamojiFunction(
                            declaration=spamoji_function()(method),
                            closure=Environment(),
                            is_initializer=False,
                        )
                        for name, method in inspect.getmembers(
                            cls, predicate=inspect.isfunction
                        )
                    },
                )

        setattr(cls, "_spamoji_emoji", emoji or cls.__name__)
        setattr(cls, "_spamoji_class", WrappedClass)
        return cls

    return decorator
