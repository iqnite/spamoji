"""
Contains the variable resolution pass for spamoji.
"""

from enum import Enum
from typing import Callable, TYPE_CHECKING

from spamoji import expr, stmt
from spamoji.token import Token

if TYPE_CHECKING:
    from spamoji.interpreter import Interpreter


class FunctionType(Enum):
    NONE = 0
    FUNCTION = 1
    METHOD = 2
    INITIALIZER = 3


class ClassType(Enum):
    NONE = 0
    CLASS = 1


class LoopType(Enum):
    NONE = 0
    WHILE = 1


class Resolver(expr.Visitor, stmt.Visitor):
    def __init__(self, interpreter: "Interpreter", error_handler: Callable) -> None:
        self.interpreter = interpreter
        self.scopes: list[dict[str, bool]] = []
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE
        self.current_loop = LoopType.NONE
        self.error_handler = error_handler

    def visit_block_stmt(self, stmt: stmt.Block) -> object:
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    def visit_class_stmt(self, stmt: stmt.Class) -> object:
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS
        self.declare(stmt.name)
        self.define(stmt.name)
        self.begin_scope()
        self.scopes[-1]["🤖"] = True
        for method in stmt.methods:
            if method.name.lexeme == "✨":
                declaration = FunctionType.INITIALIZER
            else:
                declaration = FunctionType.METHOD
            self.resolve_function(method, declaration)
        self.end_scope()
        self.current_class = enclosing_class

    def visit_expression_stmt(self, stmt: stmt.Expression) -> object:
        self.resolve(stmt.expression)

    def visit_if_stmt(self, stmt: stmt.If) -> object:
        self.resolve(stmt.condition)
        if stmt.then_branch is not None:
            self.resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

    def visit_return_stmt(self, stmt: stmt.Return) -> object:
        if self.current_function == FunctionType.NONE:
            self.error_handler(stmt.keyword.line, "Can't return from top-level code.")
            return
        if stmt.value is not None:
            if self.current_function == FunctionType.INITIALIZER:
                self.error_handler(
                    stmt.keyword, "Can't return a value from an initializer."
                )
            self.resolve(stmt.value)

    def visit_while_stmt(self, stmt: stmt.While) -> object:
        self.resolve(stmt.condition)
        enclosing_loop = self.current_loop
        self.current_loop = LoopType.WHILE
        if stmt.body is not None:
            self.resolve(stmt.body)
        self.current_loop = enclosing_loop

    def visit_loopctrl_stmt(self, stmt: stmt.LoopCtrl) -> object:
        if self.current_loop == LoopType.NONE:
            self.error_handler(
                stmt.type.line, "Can't break or continue from outside a loop."
            )

    def visit_function_stmt(self, stmt: stmt.Function) -> object:
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visit_variable_stmt(self, stmt: stmt.Variable) -> object:
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)

    def visit_assign_expr(self, expr: expr.Assign) -> object:
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_variable_expr(self, expr: expr.Variable) -> object:
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) == False:
            self.error_handler(
                expr.name.line, "Can't read local variable in its own initializer."
            )
        self.resolve_local(expr, expr.name)

    def visit_if_expr(self, expr: expr.If) -> object:
        self.resolve(expr.condition)
        self.resolve(expr.then_branch)
        self.resolve(expr.else_branch)

    def visit_binary_expr(self, expr: expr.Binary) -> object:
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_call_expr(self, expr: expr.Call) -> object:
        self.resolve(expr.callee)
        for arg in expr.arguments:
            self.resolve(arg)

    def visit_get_expr(self, expr: expr.Get) -> object:
        self.resolve(expr.obj)

    def visit_set_expr(self, expr: expr.Set) -> object:
        self.resolve(expr.value)
        self.resolve(expr.obj)

    def visit_this_expr(self, expr: expr.This) -> object:
        if self.current_class == ClassType.NONE:
            self.error_handler(expr.keyword, "Can't use '🤖' outside of a class.")
            return
        self.resolve_local(expr, expr.keyword)

    def visit_grouping_expr(self, expr: expr.Grouping) -> object:
        self.resolve(expr.expression)

    def visit_logical_expr(self, expr: expr.Logical) -> object:
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_unary_expr(self, expr: expr.Unary) -> object:
        self.resolve(expr.right)

    def resolve(self, expr_or_stmt: list[stmt.Stmt] | stmt.Stmt | expr.Expr):
        if isinstance(expr_or_stmt, stmt.Stmt):
            return self.resolve_statement(expr_or_stmt)
        if isinstance(expr_or_stmt, expr.Expr):
            return self.resolve_expression(expr_or_stmt)
        return self.resolve_statements(expr_or_stmt)

    def resolve_statements(self, statements: list[stmt.Stmt]):
        for statement in statements:
            self.resolve_statement(statement)

    def resolve_statement(self, statement: stmt.Stmt):
        statement.accept(self)

    def resolve_expression(self, expression: expr.Expr):
        expression.accept(self)

    def resolve_local(self, expression: expr.Expr, name: Token):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expression, len(self.scopes) - 1 - i)
                return

    def resolve_function(self, func: stmt.Function, type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = type
        self.begin_scope()
        for arg in func.arguments:
            self.declare(arg)
            self.define(arg)
        self.resolve(func.body)
        self.end_scope()
        self.current_function = enclosing_function

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if not self.scopes:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.error_handler(
                name.line, "Already a variable with this name in this scope."
            )
        scope[name.lexeme] = False

    def define(self, name: Token):
        if not self.scopes:
            return
        self.scopes[-1][name.lexeme] = True
