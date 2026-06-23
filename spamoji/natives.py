"""
Contains native functions.
"""

import random
import sys
import time
import typing

from spamoji.functions import spamoji_function
from spamoji.helpers import SpamojiValueError, spamoji_value_error

if typing.TYPE_CHECKING:
    from spamoji.interpreter import Interpreter


@spamoji_function("🐍")
def python_eval(code: str) -> object:
    return eval(code)


@spamoji_function("💬")
def spamoji_print(_interpreter: "Interpreter", obj: object) -> object:
    print(_interpreter.stringify(obj))
    return obj


@spamoji_function("💭")
def spamoji_print_no_newline(_interpreter: "Interpreter", obj: object) -> object:
    print(_interpreter.stringify(obj), end="")
    return obj


@spamoji_function("⌨️")
def get_user_input() -> str:
    return input()


@spamoji_function("🔢")
def convert_to_float(obj: object) -> float | SpamojiValueError:
    try:
        return float(typing.cast(float, obj))
    except ValueError:
        return spamoji_value_error


@spamoji_function("🕰️")
def get_time() -> float:
    return time.time()


@spamoji_function("⏳")
def sleep(seconds: float) -> None:
    time.sleep(seconds)


@spamoji_function("🛑")
def stop_program() -> float:
    sys.exit()


@spamoji_function("🎲")
def random_int(min: int, max: int) -> int:
    return random.randint(min, max)
