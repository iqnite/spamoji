"""
Entry point for the Spamoji interpreter.
"""

import os
import sys
from pathlib import Path

from spamoji.classes import SpamojiModule
from spamoji.helpers import SpamojiRuntimeError
from spamoji.interpreter import Interpreter
from spamoji.parser import Parser
from spamoji.resolver import Resolver
from spamoji.scanner import Scanner


class Spamoji:
    def __init__(self):
        self.interpreter = Interpreter()
        self.had_error = False
        self.had_runtime_error = False

    def main(self):
        """Main entry point.
        Gets a script file name from the command arguments, or launches the REPL."""
        if len(sys.argv) == 1:
            self.repl()
        else:
            self.run_file(sys.argv[1])

    def run_file(self, filename):
        """Runs a script file."""
        self.had_error = False
        self.had_runtime_error = False
        with open(filename, "r", encoding="utf-8") as f:
            self.run(f.read(), filename=filename)
        if self.had_error:
            sys.exit(65)
        if self.had_runtime_error:
            sys.exit(70)

    def repl(self):
        """Allows to enter commands and evaluate them interactively."""
        print("🍝 Spamoji REPL v0.2.0-development")
        print(
            "Visit https://github.com/iqnite/spamoji#readme-ov-file for help. Press Ctrl+C to exit."
        )
        try:
            while True:
                self.had_error = False
                self.had_runtime_error = False
                line = input("> ") + "\n"
                self.run(line, filename=None, print_expressions=True)
        except KeyboardInterrupt:
            sys.exit()

    def run(
        self, source: str, filename: str | None = None, print_expressions: bool = False
    ):
        """Runs a piece of code."""
        source = self.load_imports(source, filename)
        scanner = Scanner(source, self.error)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, self.report)
        statements = parser.parse()
        if self.had_error:
            return
        resolver = Resolver(self.interpreter, self.error)
        resolver.resolve(statements)
        if self.had_error:
            return
        self.interpreter.interpret(
            statements,
            print_expressions=print_expressions,
            error_handler=self.runtime_error,
        )

    def load_imports(
        self,
        source: str,
        current_file: str | None = None,
        loaded_modules: dict[str, SpamojiModule] | None = None,
    ) -> str:
        """Loads import statements into module objects and removes them from the source."""
        if loaded_modules is None:
            loaded_modules = {}

        out_lines: list[str] = []
        for raw_line in source.splitlines():
            stripped = raw_line.lstrip()
            if stripped.startswith("🧩"):
                import_target = stripped[1:].strip()
                if not import_target:
                    self.error(0, "Empty import target")
                    continue

                module = self.load_module(import_target, current_file, loaded_modules)
                if module is not None:
                    self.interpreter.globals.define(module.name, module)
                    self.interpreter.locals.update(module.locals)
            else:
                out_lines.append(raw_line)

        return "\n".join(out_lines)

    def load_module(
        self,
        import_target: str,
        current_file: str | None = None,
        loaded_modules: dict[str, SpamojiModule] | None = None,
    ) -> SpamojiModule | None:
        if loaded_modules is None:
            loaded_modules = {}

        base_dir = (
            os.getcwd()
            if current_file is None
            else os.path.dirname(os.path.abspath(current_file))
        )
        candidate = import_target
        if not os.path.isabs(candidate):
            candidate = os.path.join(base_dir, candidate)

        if not os.path.exists(candidate):
            alt = candidate + ".🍝"
            if os.path.exists(alt):
                candidate = alt

        try:
            real = os.path.abspath(candidate)
        except Exception:
            self.error(0, f"Invalid import path: {import_target}")
            return None

        if real in loaded_modules:
            return loaded_modules[real]

        if not (os.path.exists(real) and os.path.isfile(real)):
            self.error(0, f"Imported file not found: {import_target}")
            return None

        with open(real, "r", encoding="utf-8") as f:
            module_source = f.read()

        module_interpreter = Interpreter()
        module_loader = Spamoji()
        module_loader.interpreter = module_interpreter
        module_source = module_loader.load_imports(module_source, real, loaded_modules)

        scanner = Scanner(module_source, module_loader.error)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, module_loader.report)
        statements = parser.parse()
        if module_loader.had_error:
            return None

        resolver = Resolver(module_interpreter, module_loader.error)
        resolver.resolve(statements)
        if module_loader.had_error:
            return None

        module_interpreter.interpret(
            statements,
            print_expressions=False,
            error_handler=module_loader.runtime_error,
        )
        if module_loader.had_error or module_loader.had_runtime_error:
            return None

        module_name = Path(real).stem
        module = SpamojiModule(
            module_name,
            module_interpreter.globals,
            dict(module_interpreter.locals),
        )
        loaded_modules[real] = module
        return module

    def error(self, line: int, message: str):
        """Reports an error with a given message and line number."""
        self.report(line, "", message)

    def runtime_error(self, error: SpamojiRuntimeError):
        print(f"{error}\n[line {error.token.line}]")
        self.had_runtime_error = True

    def report(self, line: int, where: str, message: str):
        """Reports an error with a given message and line number."""
        self.had_error = True
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)


def main():
    Spamoji().main()


if __name__ == "__main__":
    main()
