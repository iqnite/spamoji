"""
Contains helper functions and classes for the Spamoji interpreter.
"""

import sys


def report(line: int, where: str, message: str):
    """Reports an error with a given message and line number."""
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)


def error(line: int, message: str):
    """Reports an error with a given message and line number."""
    report(line, "", message)
