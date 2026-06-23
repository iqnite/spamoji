"""
Contains native functions.
"""

import importlib
import importlib.util
import pathlib
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


@spamoji_function("🐍🧩")
def python_import(_interpreter: "Interpreter", module_path: str) -> object:
    path = pathlib.Path(module_path).resolve()
    added_to_sys_path = False
    module_name = path.stem
    cwd = str(pathlib.Path.cwd())
    if cwd not in sys.path:
        sys.path.insert(0, cwd)
        added_to_sys_path = True
    try:
        spec = importlib.util.spec_from_file_location(module_name, str(path))
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load the module from {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        _interpreter.define_natives(module)
        return module
    finally:
        if added_to_sys_path:
            sys.path.remove(cwd)


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
def random_int(min: int | float, max: int | float) -> int:
    return random.randint(int(min), int(max))
