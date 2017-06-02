# -*- coding:utf-8 -*-

from ast import *


class Precedence:
    LEFT, RIGHT = range(2)

    def __init__(self, value, assoc):
        self.value = value
        self.assoc = assoc


class Parser:
    def __init__(self, lex):
        self.lexer = lex
        self.operators = {
            '=': Precedence(1, Precedence.RIGHT),
            '<': Precedence(2, Precedence.LEFT),
            '<=': Precedence(2, Precedence.LEFT),
            '>': Precedence(2, Precedence.LEFT),
            '>=': Precedence(2, Precedence.LEFT),
            '==': Precedence(2, Precedence.LEFT),
            '!=': Precedence(2, Precedence.LEFT),
            '+': Precedence(3, Precedence.LEFT),
            '-': Precedence(3, Precedence.LEFT),
            '*': Precedence(4, Precedence.LEFT),
            '/': Precedence(4, Precedence.LEFT),
            '%': Precedence(4, Precedence.LEFT),
        }

    def _is_token(self, image):
        token = self.lexer.peek()
        return image == token.image

    def _consume_token(self, image):
        token = self.lexer.read()
        if image != token.image:
            raise Exception("can't consume token: '" + image + "', read: " + token.image)

    def _next_op_prec(self):
        token = self.lexer.peek()
        return self.operators.get(token.image) if token.id is not None else None

    def primary(self):
        if self._is_token('('):
            self._consume_token('(')
            e = self.expr()
            self._consume_token(')')
            return e
        token = self.lexer.read()
        if token.value is not None:
            return NumberLeaf(token)
        elif token.str is not None:
            return StringLeaf(token)
        elif token.id is not None:
            return NameLeaf(token)

    def factor(self):
        if self._is_token('-'):
            op = ASTLeaf(self.lexer.read())
            right = self.primary()
            return UnaryAST(op, right)
        return self.primary()

    def expr(self):
        right = self.primary()
        next_prec = self._next_op_prec()
        while next_prec is not None:
            right = self._do_shift(right, next_prec.value)
            next_prec = self._next_op_prec()
        return right

    @staticmethod
    def _right_is_expr(prec, next_prec):
        if next_prec.assoc == Precedence.LEFT:
            return prec < next_prec.value
        return prec <= next_prec.value

    def _do_shift(self, left, prec):
        op = ASTLeaf(self.lexer.read())
        right = self.primary()
        next_prec = self._next_op_prec()
        while next_prec is not None and self._right_is_expr(prec, next_prec):
            right = self._do_shift(right, next_prec.value)
            next_prec = self._next_op_prec()
        return BinaryAST(left, op, right)

    def _block(self):
        while True:
            if self._is_token(';'):
                self._consume_token(';')
            elif self._is_token(r'\n'):
                self._consume_token(r'\n')
            else:
                break
        while not self._is_token('}'):
            statement = self.statement()
            while True:
                if self._is_token(';'):
                    self._consume_token(';')
                elif self._is_token(r'\n'):
                    self._consume_token(r'\n')
                else:
                    break
            if statement is not None:
                yield statement

    def block(self):
        if self._is_token('{'):
            self._consume_token('{')
            ast = ASList(*self._block())
            self._consume_token('}')
            return ast
        raise Exception("parse error")

    def statement(self):
        if self._is_token('if'):
            token = self.lexer.read()
            args = [ASTLeaf(token), self.expr(), self.block()]
            if self._is_token('else'):
                token = self.lexer.read()
                args.extend([ASTLeaf(token), self.block()])
            return IfAST(*args)
        elif self._is_token('while'):
            token = self.lexer.read()
            return WhileAST(ASTLeaf(token), self.expr(), self.block())
        elif self._is_token('print'):
            token = self.lexer.read()
            return PrintAST(ASTLeaf(token), self.expr())
        elif self._is_token('log'):
            token = self.lexer.read()
            return LogAST(ASTLeaf(token), self.expr())
        return self.expr()

    def _program(self):
        while self.lexer.peek().line_no != -1:
            while True:
                if self._is_token(';'):
                    self._consume_token(';')
                elif self._is_token(r'\n'):
                    self._consume_token(r'\n')
                else:
                    break
            yield self.statement()

    def program(self):
        return ASList(*self._program())
