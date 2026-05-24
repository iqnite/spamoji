"""
Contains the actual interpreter.
"""

import typing

from spamoji import expr, stmt
from spamoji.classes import SpamojiClass, SpamojiInstance
from spamoji.functions import (
    BreakLoop,
    ContinueLoop,
    Return,
    SpamojiCallable,
    SpamojiFunction,
)
from spamoji.environment import Environment
from spamoji.expr import Binary, Expr, Grouping, Literal, Unary
from spamoji.helpers import (
    SpamojiRuntimeError,
    spamojiValueError,
)
from spamoji.natives import (
    Clock,
    ConvertToNumber,
    GetUserInput,
    Print,
    PrintNoNewline,
    PythonCall,
    Sleep,
    StopProgram,
    Randint,
)
from spamoji.token import Token, TokenType


class Interpreter(expr.Visitor, stmt.Visitor):
    """Interpreter for the Spamoji language. Evaluates an AST and produces a result."""

    def __init__(self):
        super().__init__()
        self.globals = Environment()
        self.locals: dict[Expr, int] = {}
        self.environment = self.globals
        self.print_expressions = False
        self.prints = []
        self.define_natives()

    def interpret(
        self,
        statements: list[stmt.Stmt],
        print_expressions: bool = False,
        error_handler: typing.Callable[[SpamojiRuntimeError], typing.Any] | None = None,
    ):
        self.print_expressions = print_expressions
        self.prints = []
        try:
            for statement in statements:
                self.execute(statement)
                if self.print_expressions and self.prints:
                    print(self.stringify(self.prints.pop()))
        except SpamojiRuntimeError as exc:
            if error_handler:
                error_handler(exc)

    def define_natives(self):
        self.globals.define("⚠️", spamojiValueError)
        self.globals.define("🐍", PythonCall())
        self.globals.define("💬", Print())
        self.globals.define("💭", PrintNoNewline())
        self.globals.define("⌨️", GetUserInput())
        self.globals.define("🔢", ConvertToNumber())
        self.globals.define("🕰️", Clock())
        self.globals.define("⏳", Sleep())
        self.globals.define("🛑", StopProgram())
        self.globals.define("🎲", Randint())

    def visit_literal_expr(self, expr: Literal) -> object:
        return expr.value

    def visit_unary_expr(self, expr: Unary) -> object:
        right = self.evaluate(expr.right)
        match expr.operator.token_type:
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, right)
                return -typing.cast(float, right)
            case TokenType.NOT:
                return not self.is_truthy(right)
            case _:
                return None

    def visit_variable_expr(self, expr: expr.Variable) -> object:
        return self.look_up_variable(expr.name, expr)

    def look_up_variable(self, name: Token, expression: Expr):
        distance = self.locals.get(expression)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        return self.globals.get(name)

    def check_number_operands(self, operator: Token, *operands: object):
        for operand in operands:
            if not isinstance(operand, float):
                raise SpamojiRuntimeError(operator, "Operands must be numbers.")

    def is_truthy(self, obj: object) -> bool:
        if obj is None:
            return False
        if obj is spamojiValueError:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def stringify(self, obj: object) -> str:
        if obj is None:
            return "🫥"
        text = str(obj)
        if isinstance(obj, float):
            if text.endswith(".0"):
                return text[:-2]
        if isinstance(obj, bool):
            return "✅" if obj else "❌"
        if obj is spamojiValueError:
            return "⚠️"
        return text

    def visit_grouping_expr(self, expr: Grouping) -> object:
        return self.evaluate(expr.expression)

    def evaluate(self, expr: Expr) -> object:
        result = expr.accept(self)
        if self.print_expressions:
            self.prints.append(result)
        return result

    def execute(self, stmt: stmt.Stmt) -> object:
        return stmt.accept(self)

    def resolve(self, expr: Expr, depth: int):
        self.locals[expr] = depth

    def execute_block(self, statements: list[stmt.Stmt], environment: Environment):
        previous_environment = self.environment
        try:
            self.environment = environment
            for statement in statements:
                try:
                    self.execute(statement)
                except (BreakLoop, ContinueLoop) as e:
                    raise e
        finally:
            self.environment = previous_environment

    def visit_block_stmt(self, stmt: stmt.Block) -> object:
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_class_stmt(self, stmt: stmt.Class) -> object:
        self.environment.define(stmt.name.lexeme, None)
        methods = {}
        for method in stmt.methods:
            func = SpamojiFunction(method, self.environment)
            methods[method.name.lexeme] = func
        new_class = SpamojiClass(stmt.name.lexeme, methods)
        self.environment.assign(stmt.name, new_class)

    def visit_expression_stmt(self, stmt: stmt.Expression) -> object:
        return self.evaluate(stmt.expression)

    def visit_function_stmt(self, stmt: stmt.Function) -> object:
        func = SpamojiFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, func)

    def visit_if_stmt(self, stmt: stmt.If) -> object:
        if self.is_truthy(self.evaluate(stmt.condition)):
            if stmt.then_branch:
                return self.execute(stmt.then_branch)
        elif stmt.else_branch:
            return self.execute(stmt.else_branch)

    def visit_while_stmt(self, stmt: stmt.While) -> object:
        while self.is_truthy(self.evaluate(stmt.condition)):
            try:
                if stmt.body is not None:
                    self.execute(stmt.body)
            except BreakLoop:
                break
            except ContinueLoop:
                continue

    def visit_return_stmt(self, stmt: stmt.Return) -> object:
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise Return(value)

    def visit_loopctrl_stmt(self, stmt: stmt.LoopCtrl) -> object:
        match stmt.type.token_type:
            case TokenType.BREAK:
                raise BreakLoop
            case TokenType.CONTINUE:
                raise ContinueLoop

    def visit_variable_stmt(self, stmt: stmt.Variable) -> object:
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return value

    def visit_assign_expr(self, expr: expr.Assign) -> object:
        value = self.evaluate(expr.value)
        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

    def visit_if_expr(self, expr: expr.If) -> object:
        return (
            self.evaluate(expr.then_branch)
            if self.is_truthy(self.evaluate(expr.condition))
            else self.evaluate(expr.else_branch)
        )

    def visit_binary_expr(self, expr: Binary) -> object:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        left_f = typing.cast(float, left)
        right_f = typing.cast(float, right)
        match expr.operator.token_type:
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left_f - right_f
            case TokenType.MULTIPLY:
                self.check_number_operands(expr.operator, left, right)
                return left_f * right_f
            case TokenType.DIVIDE:
                self.check_number_operands(expr.operator, left, right)
                try:
                    return left_f / right_f
                except ZeroDivisionError:
                    return spamojiValueError
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                if isinstance(left, str) or isinstance(right, str):
                    return self.stringify(left) + self.stringify(right)
                raise SpamojiRuntimeError(
                    expr.operator, "Operands must be numbers or strings."
                )
            case TokenType.GREATER_THAN:
                self.check_number_operands(expr.operator, left, right)
                return left_f > right_f
            case TokenType.LESS_THAN:
                self.check_number_operands(expr.operator, left, right)
                return left_f < right_f
            case TokenType.EQUALS:
                return left == right
            case TokenType.NOT_EQUALS:
                return left != right
            case TokenType.AND:
                return self.is_truthy(left) and self.is_truthy(right)
            case TokenType.OR:
                return self.is_truthy(left) or self.is_truthy(right)
            case _:
                return None

    def visit_call_expr(self, expr: expr.Call) -> object:
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        if not isinstance(callee, SpamojiCallable):
            raise SpamojiRuntimeError(expr.paren, "Can only call functions.")
        func = typing.cast(SpamojiCallable, callee)
        if (got_args := len(arguments)) != (expected_args := func.arity()):
            raise SpamojiRuntimeError(
                expr.paren, f"Expected {expected_args} arguments but got {got_args}."
            )
        try:
            return func.call(self, arguments)
        except (TypeError, ValueError, OverflowError) as e:
            raise SpamojiRuntimeError(expr.paren, e.args[0]) from e

    def visit_get_expr(self, expr: expr.Get) -> object:
        obj = self.evaluate(expr.obj)
        if isinstance(obj, SpamojiInstance):
            return typing.cast(SpamojiInstance, obj).get(expr.name)
        raise SpamojiRuntimeError(expr.name, "Only instances have properties.")

    def visit_set_expr(self, expr: expr.Set) -> object:
        obj = self.evaluate(expr.obj)
        if not isinstance(obj, SpamojiInstance):
            raise SpamojiRuntimeError(expr.name, "Only instances have fields.")
        value = self.evaluate(expr.value)
        typing.cast(SpamojiInstance, obj).set(expr.name, value)
        return value
    
    def visit_this_expr(self, expr: expr.This) -> object:
        return self.look_up_variable(expr.keyword, expr)

    def visit_logical_expr(self, expr: expr.Logical) -> object:
        left = self.evaluate(expr.left)
        if expr.operator.token_type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.evaluate(expr.right)
