"""
Contains the base construct for Spamoji classes
"""

import inspect
from typing import TYPE_CHECKING
import typing

from spamoji.environment import Environment
from spamoji.expr import Expr
from spamoji.functions import SpamojiCallable, SpamojiFunction
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


class SpamojiNativeInstance(SpamojiInstance):
    def __init__(self, my_class: SpamojiClass, native_obj: object):
        super().__init__(my_class)
        self.native_obj = native_obj

    def get(self, name: Token) -> object:
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        method = self.my_class.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)
        if hasattr(self.native_obj, name.lexeme):
            attr = getattr(self.native_obj, name.lexeme)
            if inspect.isroutine(attr) or inspect.isfunction(attr):
                return SpamojiNativeMethod(attr, self)
            return attr
        raise SpamojiRuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name: Token, value: object):
        self.fields[name.lexeme] = value
        try:
            setattr(self.native_obj, name.lexeme, value)
        except (AttributeError, TypeError):
            pass

    def __str__(self) -> str:
        return str(self.native_obj)


class SpamojiNativeMethod(SpamojiFunction):
    def __init__(
        self,
        func: typing.Callable,
        instance: typing.Any = None,
        is_initializer: bool = False,
    ):
        self.func = func
        self.instance = instance
        self.is_initializer = is_initializer
        try:
            self.parameters = inspect.signature(func).parameters
        except (ValueError, TypeError):
            self.parameters = {}
        self.has_self = "self" in self.parameters

    def bind(self, instance: typing.Any) -> "SpamojiNativeMethod":
        return SpamojiNativeMethod(self.func, instance, self.is_initializer)

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        args = list(arguments)
        if self.instance is not None and self.has_self:
            target = getattr(self.instance, "native_obj", self.instance)
            args.insert(0, target)
        if "_interpreter" in self.parameters:
            idx = list(self.parameters).index("_interpreter")
            args.insert(idx, interpreter)
        result = self.func(*args)
        if self.is_initializer:
            return self.instance
        if result is not None and hasattr(type(result), "_spamoji_callable"):
            callable_cls = getattr(type(result), "_spamoji_callable")
            if isinstance(callable_cls, SpamojiClass) and not isinstance(
                result, SpamojiInstance
            ):
                return SpamojiNativeInstance(callable_cls, result)
        return result

    def arity(self) -> int:
        count = len(self.parameters)
        if "_interpreter" in self.parameters:
            count -= 1
        if self.has_self:
            count -= 1
        return max(0, count)

    def __str__(self) -> str:
        name = getattr(
            self.func,
            "_spamoji_emoji",
            getattr(self.func, "__name__", "native_method"),
        )
        return f"<⚙️ {name}>"


class SpamojiNativeClass(SpamojiClass):
    def __init__(
        self,
        cls: type,
        name: str,
        superclasses: list[SpamojiClass],
        methods: dict[str, SpamojiFunction],
    ):
        super().__init__(name, superclasses, methods)
        self.cls = cls
        try:
            self.init_parameters = inspect.signature(cls.__init__).parameters
        except (ValueError, TypeError):
            self.init_parameters = {}

    def arity(self) -> int:
        init_method = self.find_method("✨")
        if (
            init_method is not None
            and getattr(init_method, "func", None) is not object.__init__
        ):
            return init_method.arity()
        count = len(self.init_parameters)
        if "self" in self.init_parameters:
            count -= 1
        if "_interpreter" in self.init_parameters:
            count -= 1
        return max(0, count)

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        args = list(arguments)
        if "_interpreter" in self.init_parameters:
            idx = list(self.init_parameters).index("_interpreter")
            args.insert(idx, interpreter)
        native_obj = self.cls(*args)
        if isinstance(native_obj, SpamojiInstance):
            return native_obj
        return SpamojiNativeInstance(self, native_obj)


def spamoji_class(emoji_or_cls: str | None = None) -> typing.Callable:
    """
    Decorator to mark a class as a Spamoji native class.
    The class will be registered as a native class in the Spamoji interpreter.
    If the emoji parameter is provided, it will be used as the class's emoji name.

    Example usage:
    @spamoji_class("🎁")
    class MyNativeClass:
        pass
    """

    def decorator(cls: typing.Type) -> typing.Type:
        if hasattr(cls, "_spamoji_callable") and isinstance(
            getattr(cls, "_spamoji_callable"), SpamojiClass
        ):
            return cls

        methods: dict[str, SpamojiFunction] = {}
        for base in reversed(cls.__mro__[:-1]):
            for attr_name, member in base.__dict__.items():
                if inspect.isroutine(member) or inspect.isfunction(member):
                    emoji_name = getattr(member, "_spamoji_emoji", None)
                    is_init = attr_name == "__init__" or emoji_name == "✨"
                    native_method = SpamojiNativeMethod(member, is_initializer=is_init)
                    if emoji_name:
                        methods[emoji_name] = native_method
                    if is_init:
                        methods["✨"] = native_method
                    methods[attr_name] = native_method

        superclasses = []
        for superclass in cls.__bases__:
            if superclass is not object and superclass.__module__ != "builtins":
                if not hasattr(superclass, "_spamoji_callable"):
                    try:
                        spamoji_class()(superclass)
                    except TypeError:
                        pass
                sc = getattr(superclass, "_spamoji_callable", None)
                if isinstance(sc, SpamojiClass):
                    superclasses.append(sc)

        cls_emoji = emoji if isinstance(emoji_or_cls, str) else None
        class_name = cls_emoji or getattr(cls, "_spamoji_emoji", None) or cls.__name__
        native_class = SpamojiNativeClass(
            cls=cls,
            name=class_name,
            superclasses=superclasses,
            methods=methods,
        )

        try:
            setattr(cls, "_spamoji_emoji", class_name)
            setattr(cls, "_spamoji_callable", native_class)
            setattr(cls, "_spamoji_class", native_class)
        except TypeError:
            pass
        return cls

    if isinstance(emoji_or_cls, type):
        emoji = None
        return decorator(emoji_or_cls)
    emoji = emoji_or_cls
    return decorator
