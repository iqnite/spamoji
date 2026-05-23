"""
Contains the variable resolution pass for spamoji.
"""

from typing import TYPE_CHECKING

from spamoji import expr, stmt
from spamoji.token import Token

if TYPE_CHECKING:
    from spamoji.interpreter import Interpreter


class Resolver(expr.Visitor, stmt.Visitor):
    def __init__(self, interpreter: "Interpreter") -> None:
        self.interpreter = interpreter
        self.scopes: list[dict[str, bool]] = []

    def visit_block_stmt(self, stmt: stmt.Block) -> object:
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    def visit_variable_stmt(self, stmt: stmt.Variable) -> object:
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)

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

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if not self.scopes:
            return
        scope = self.scopes[-1]
        scope[name.lexeme] = False

    def define(self, name: Token):
        if not self.scopes:
            return
        self.scopes[-1][name.lexeme] = True
