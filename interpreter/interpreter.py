"""
Contains the actual interpreter.
"""

import typing

from interpreter import expr, stmt
from interpreter.environment import Environment
from interpreter.expr import Binary, Expr, Grouping, Literal, Unary
from interpreter.helpers import SpamojiRuntimeError
from interpreter.token import Token, TokenType


class Interpreter(expr.Visitor, stmt.Visitor):
    """Interpreter for the Spamoji language. Evaluates an AST and produces a result."""

    def __init__(self):
        super().__init__()
        self.environment = Environment()

    def interpret(
        self,
        statements: list[stmt.Stmt],
        error_handler: typing.Callable[[SpamojiRuntimeError], typing.Any],
    ):
        try:
            for statement in statements:
                self.execute(statement)
        except SpamojiRuntimeError as exc:
            error_handler(exc)

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
        return self.environment.get(expr.name)

    def check_number_operands(self, operator: Token, *operands: object):
        for operand in operands:
            if not isinstance(operand, float):
                raise SpamojiRuntimeError(operator, "Operands must be numbers.")

    def is_truthy(self, obj: object) -> bool:
        if obj is None:
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
        return text

    def visit_grouping_expr(self, expr: Grouping) -> object:
        return self.evaluate(expr.expression)

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def execute(self, stmt: stmt.Stmt) -> object:
        return stmt.accept(self)

    def visit_expression_stmt(self, stmt: stmt.Expression) -> object:
        return self.evaluate(stmt.expression)

    def visit_python_stmt(self, stmt: stmt.Python) -> object:
        value = self.evaluate(stmt.expression)
        return eval(typing.cast(str, value))

    def visit_variable_stmt(self, stmt: stmt.Variable) -> object:
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return value

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
                    return "⚠️"
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
