"""
Parser for the Spamoji language. Converts a list of tokens into an abstract syntax tree (AST).
"""

import typing

from interpreter import expr, stmt
from interpreter.expr import Binary, Expr, Grouping, Literal, Logical, Unary
from interpreter.stmt import Block, Stmt
from interpreter.helpers import error_token
from interpreter.token import Token, TokenType


class ParseError(Exception):
    """Exception class for parse errors."""

    pass


class Parser:
    """Parser for the Spamoji language. Converts a list of tokens into an AST."""

    def __init__(
        self,
        tokens: list[Token],
        error_handler: typing.Callable[[int, str, str], typing.Any] | None = None,
    ):
        """
        Initializes the parser with a list of tokens.
        :param list[Token] tokens: The list of tokens to parse.
        """
        self.tokens = tokens
        self.current = 0
        self.error_handler = error_handler

    def parse(self) -> list[Stmt]:
        """Parses the tokens and returns the resulting AST."""
        statements = []
        while not self.is_at_end():
            while self.peek().token_type == TokenType.NEWLINE and not self.is_at_end():
                self.advance()
            if self.is_at_end():
                break
            statements.append(self.declaration())
        return statements

    def expression(self) -> Expr:
        """Parses an expression."""
        return self.assignment()

    def block(self) -> list[Stmt]:
        statements = []
        block_indent = typing.cast(int, self.previous().literal)
        while not self.is_at_end():
            while self.peek().token_type == TokenType.NEWLINE:
                self.advance()
            if self.is_at_end():
                return statements
            if self.peek().token_type == TokenType.INDENT:
                self.advance()
                current_indent = typing.cast(int, self.previous().literal)
                if current_indent < block_indent:
                    self.current -= 1
                    return statements
                if current_indent > block_indent:
                    statements.append(Block(self.block()))
            elif statements:
                return statements
            statements.append(self.declaration())
        return statements

    def declaration(self) -> Stmt | None:
        try:
            if self.match(TokenType.FUNCTION):
                return self.function("function")
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def statement(self) -> Stmt:
        """Parses a statement."""
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.BREAK, TokenType.CONTINUE):
            return self.loop_control_statement()
        if self.match(TokenType.INDENT):
            return Block(self.block())
        return self.expression_statement()

    def if_statement(self) -> Stmt:
        then_branch = else_branch = None
        condition = self.expression()
        self.consume("Expect newline after if condition.", TokenType.NEWLINE)
        while self.peek().token_type == TokenType.NEWLINE:
            self.advance()
        if self.match_indented(TokenType.IFTRUE):
            while self.peek().token_type == TokenType.NEWLINE:
                self.advance()
            then_branch = self.statement()
        while self.peek().token_type == TokenType.NEWLINE:
            self.advance()
        if self.match_indented(TokenType.ELSE):
            while self.peek().token_type == TokenType.NEWLINE:
                self.advance()
            else_branch = self.statement()
        return stmt.If(condition, then_branch, else_branch)

    def while_statement(self) -> Stmt:
        condition = self.expression()
        self.consume("Expect newline after while condition.", TokenType.NEWLINE)
        body = self.statement()
        return stmt.While(condition, body)

    def match_indented(self, token_type: TokenType) -> bool:
        if (
            self.check(TokenType.INDENT)
            and self.current + 1 < len(self.tokens)
            and self.tokens[self.current + 1].token_type == token_type
        ):
            self.advance()
            self.advance()
            return True
        return self.match(token_type)

    def return_statement(self) -> Stmt:
        keyword = self.previous()
        value = None
        if not self.check(TokenType.NEWLINE):
            value = self.expression()
        self.consume("Cannot return more than 1 value.", TokenType.NEWLINE)
        return stmt.Return(keyword, value)

    def loop_control_statement(self) -> Stmt:
        return stmt.LoopCtrl(self.previous())

    def var_declaration(self) -> Stmt:
        name = self.consume("Except variable name.", TokenType.IDENTIFIER)
        initializer = None
        if self.match(TokenType.ASSIGNMENT):
            initializer = self.expression()
        return stmt.Variable(name, initializer)

    def expression_statement(self) -> Stmt:
        expr = self.expression()
        self.consume("Expect 1 statement per line", TokenType.NEWLINE, TokenType.EOF)
        return stmt.Expression(expr)

    def function(self, kind: str):
        name = self.consume(f"Expect {kind} name.", TokenType.IDENTIFIER)
        self.consume(f"Expect '🫸' or '❗' after {kind} name.")
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                arguments.append(
                    self.consume("Expect argument name.", TokenType.IDENTIFIER)
                )
                if not self.match(TokenType.COMMA):
                    break
        self.consume("Expect '🫷' after arguments.", TokenType.RIGHT_PAREN)
        self.consume(f"Expect newline before {kind} body.", TokenType.NEWLINE)
        body = self.block()
        return stmt.Function(name, arguments, body)

    def assignment(self) -> Expr:
        expression = self.ternary()
        if self.match(TokenType.ASSIGNMENT):
            assignment_operator = self.previous()
            value = self.assignment()
            if isinstance(expression, expr.Variable):
                name = expression.name
                return expr.Assign(name, value)
            self.error(assignment_operator, "Invalid assignment target.")
        return expression

    def ternary(self) -> Expr:
        if self.match(TokenType.IF):
            condition = self.expression()
            self.consume(
                "Expect '👍' after condition in 🤔 expression.",
                TokenType.IFTRUE,
            )
            then_branch = self.expression()
            self.consume(
                "Expect '👎' branch for 🤔 expression.",
                TokenType.ELSE,
            )
            else_branch = self.expression()
            return expr.If(condition, then_branch, else_branch)
        return self.logic_or()

    def equality(self) -> Expr:
        """Parses an equality expression."""
        expr = self.comparison()
        while self.match(TokenType.NOT_EQUALS, TokenType.EQUALS):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def match(self, *types: TokenType) -> bool:
        """Checks if the current token matches any of the given types."""
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, *token_types: TokenType) -> bool:
        """Checks if the current token is of any of the given types."""
        if self.is_at_end():
            return False
        return self.peek().token_type in token_types

    def advance(self) -> Token:
        """Advances to the next token and returns the previous one."""
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        """Checks if we've reached the end of the token list."""
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token:
        """Returns the current token without advancing."""
        return self.tokens[self.current]

    def previous(self) -> Token:
        """Returns the most recently consumed token."""
        return self.tokens[self.current - 1]

    def logic_or(self) -> Expr:
        expr = self.logic_and()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.logic_and()
            expr = Logical(expr, operator, right)
        return expr

    def logic_and(self) -> Expr:
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(TokenType.GREATER_THAN, TokenType.LESS_THAN):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while True:
            if self.match(TokenType.PLUS, TokenType.MINUS):
                operator = self.previous()
                right = self.factor()
                expr = Binary(expr, operator, right)
                continue
            if self.can_implicitly_concatenate(expr):
                operator = Token(TokenType.PLUS, "➕", None, self.peek().line)
                right = self.factor()
                expr = Binary(expr, operator, right)
                continue
            break
        return expr

    def can_implicitly_concatenate(self, expr: Expr) -> bool:
        if self.is_string_expr(expr):
            return self.starts_value(self.peek().token_type)
        return self.peek().token_type == TokenType.STRING

    def is_string_expr(self, expr: Expr) -> bool:
        if isinstance(expr, Literal):
            return isinstance(expr.value, str)
        if isinstance(expr, Grouping):
            return self.is_string_expr(expr.expression)
        if isinstance(expr, Unary):
            return self.is_string_expr(expr.right)
        if isinstance(expr, Binary):
            return self.is_string_expr(expr.left) or self.is_string_expr(expr.right)
        return False

    def starts_value(self, token_type: TokenType) -> bool:
        return token_type in (
            TokenType.LEFT_PAREN,
            TokenType.NUMBER,
            TokenType.STRING,
            TokenType.TRUE,
            TokenType.FALSE,
            TokenType.NULL,
            TokenType.IDENTIFIER,
        )

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.MINUS, TokenType.NOT):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.call()

    def call(self) -> Expr:
        expression = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expression = self.finish_call(expression)
            else:
                break
        return expression

    def finish_call(self, callee: Expr) -> Expr:
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        paren = self.consume("Expect '🫷' after arguments.", TokenType.RIGHT_PAREN)
        return expr.Call(callee, paren, arguments)

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NULL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return expr.Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expression = self.expression()
            self.consume("Expect '🫷' after expression.", TokenType.RIGHT_PAREN)
            return Grouping(expression)
        raise self.error(self.peek(), "Expected expression.")

    def consume(self, message: str, *token_types: TokenType) -> Token:
        if self.check(*token_types):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str) -> ParseError:
        if self.error_handler:
            error_token(token, message, self.error_handler)
        return ParseError()

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().token_type == TokenType.NEWLINE:
                return
            if self.peek().token_type in (
                TokenType.FUNCTION,
                TokenType.VAR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.RETURN,
            ):
                return
            self.advance()
