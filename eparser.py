# -*- coding:utf-8 -*-


class Parser:
    class Precedence:
        def __init__(self, value, left_assoc):
            self.value = value
            self.left_assoc = left_assoc

    def __init__(self, lex):
        self.lexer = lex
        self.operators = {
            '+': self.Precedence(2, True),
            '-': self.Precedence(2, True),
            '*': self.Precedence(3, True),
            '/': self.Precedence(3, True),
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
            return ASTLeaf(token)
        # raise Exception("parse error")

    def factor(self):
        if self._is_token('-'):
            op = ASTLeaf(self.lexer.read())
            right = self.primary()
            return ASList(op, right)
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
        if next_prec.left_assoc:
            return prec < next_prec.value
        return prec <= next_prec.value

    def _do_shift(self, left, prec):
        op = ASTLeaf(self.lexer.read())
        right = self.primary()
        next_prec = self._next_op_prec()
        while next_prec is not None and self._right_is_expr(prec, next_prec):
            right = self._do_shift(right, next_prec.value)
            next_prec = self._next_op_prec()
        return ASList(left, op, right)

    def block(self):
        if self._is_token('{'):
            self._consume_token('{')

            self._consume_token('}')
            return
        raise Exception("parse error")

    def statement(self):
        if self._is_token('if'):
            pass
        if self._is_token('while'):
            pass
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
            yield self.expr()

    def program(self):
        return ASList(*self._program())


class AST:
    def __init__(self):
        pass


class ASList(AST):
    def __init__(self, *args):
        AST.__init__(self)
        self.children = args
        if len(args) == 2:
            self.op = args[0].id
            self.right = args[1]
        elif len(args) == 3:
            self.left = args[0]
            self.op = args[1].id
            self.right = args[2]
        else:
            pass

    def __str__(self):
        return '(' + ' '.join(map(str, self.children)) + ')'

    def is_unary_op(self):
        return len(self.children) == 2

    def is_binary_op(self):
        return len(self.children) == 3


class ASTLeaf(AST):
    def __init__(self, token):
        AST.__init__(self)
        self.token = token
        self.value = token.value
        self.str = token.str
        self.id = token.id

    def __str__(self):
        return self.token.image



