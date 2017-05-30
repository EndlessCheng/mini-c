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

    @staticmethod
    def _right_is_expr(prec, next_prec):
        if next_prec.left_assoc:
            return prec < next_prec.value
        return prec <= next_prec.value

    def expression(self):
        right = self.factor()
        next_prec = self._next_op_prec()
        while next_prec is not None:
            right = self._do_shift(right, next_prec.value)
            next_prec = self._next_op_prec()
        return right

    def _do_shift(self, left, prec):
        op = ASTLeaf(self.lexer.read())
        right = self.factor()
        next_prec = self._next_op_prec()
        while next_prec is not None and self._right_is_expr(prec, next_prec):
            right = self._do_shift(right, next_prec.value)
            next_prec = self._next_op_prec()
        return ASList(left, op, right)

    def factor(self):
        if self._is_token('('):
            self._consume_token('(')
            e = self.expression()
            self._consume_token(')')
            return e
        token = self.lexer.read()
        if token.value is not None:
            return ASTLeaf(token)
        raise Exception('parse error')


class AST:
    def __init__(self):
        pass


class ASList(AST):
    def __init__(self, *args):
        AST.__init__(self)
        self.children = args
        self.left = args[0]
        self.op = args[1].id
        self.right = args[2]
        # print args[0]

    def __str__(self):
        return '(' + ' '.join(map(str, self.children)) + ')'


class ASTLeaf(AST):
    def __init__(self, token):
        AST.__init__(self)
        self.token = token
        self.value = token.value
        self.str = token.str
        self.id = token.id

    def __str__(self):
        return self.token.image
