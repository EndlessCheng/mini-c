# -*- coding:utf-8 -*-


class AST(object):
    # LIST, PRINT, UNARY, BINARY, IF, WHILE = range(6)
    FALSE = 0
    TRUE = 1

    def eval(self, env):
        raise NotImplementedError("Class %s doesn't implement eval()" % self.__class__.__name__)


class ASTLeaf(AST):
    def __init__(self, token):
        self.token = token
        self.id = token.id

    def __str__(self):
        return self.token.image

    def eval(self, env):
        raise NotImplementedError("Class %s doesn't implement eval()" % self.__class__.__name__)


class NumberLeaf(ASTLeaf):
    def __init__(self, token):
        ASTLeaf.__init__(self, token)
        self.value = token.value

    def eval(self, env):
        return self.value


class StringLeaf(ASTLeaf):
    def __init__(self, token):
        ASTLeaf.__init__(self, token)
        self.str = token.str

    def eval(self, env):
        return self.str


class NameLeaf(ASTLeaf):
    def __init__(self, token):
        ASTLeaf.__init__(self, token)
        self.id = token.id

    def eval(self, env):
        return env.values[self.id]


class ASList(AST):
    def __init__(self, *args):
        self.children = args

    def __str__(self):
        return '(' + ' '.join(map(str, self.children)) + ')'

    def eval(self, env):
        for ast in self.children:
            ast.eval(env)


class PrintAST(ASList):
    def __init__(self, *args):
        ASList.__init__(self, *args)
        self.expr = args[1]

    def eval(self, env):
        result = self.expr.eval(env)
        print result


class UnaryAST(ASList):
    def __init__(self, *args):
        ASList.__init__(self, *args)
        self.op = args[0].id
        self.right = args[1]

    def eval(self, env):
        if self.op == '-':
            return - self.right.eval()
        else:
            raise Exception("bad type for -")


class BinaryAST(ASList):
    def __init__(self, *args):
        ASList.__init__(self, *args)
        self.left = args[0]
        self.op = args[1].id
        self.right = args[2]

    def eval(self, env):
        if self.op == '=':
            right = self.right.eval(env)
            env.values[self.left.id] = right
            return right
        else:
            left = self.left.eval(env)
            right = self.right.eval(env)
            if self.op == '<':
                return AST.TRUE if left < right else AST.FALSE
            elif self.op == '<=':
                return AST.TRUE if left <= right else AST.FALSE
            elif self.op == '>':
                return AST.TRUE if left > right else AST.FALSE
            elif self.op == '>=':
                return AST.TRUE if left >= right else AST.FALSE
            elif self.op == '==':
                return AST.TRUE if left == right else AST.FALSE
            elif self.op == '!=':
                return AST.TRUE if left != right else AST.FALSE
            elif self.op == '+':
                return left + right
            elif self.op == '-':
                return left - right
            elif self.op == '*':
                return left * right
            elif self.op == '/':
                return left / right
            elif self.op == '%':
                return left % right
            else:
                raise Exception("bad operator: " + self.op)


class IfAST(ASList):
    def __init__(self, *args):
        ASList.__init__(self, *args)
        self.expr = args[1]
        self.if_block = args[2]
        self.else_block = None
        if len(args) == 5:
            self.else_block = args[4]

    def eval(self, env):
        if self.expr.eval(env) == AST.TRUE:
            self.if_block.eval(env)
        elif self.else_block is not None:
            self.else_block.eval(env)


class WhileAST(ASList):
    def __init__(self, *args):
        ASList.__init__(self, *args)
        self.expr = args[1]
        self.block = args[2]

    def eval(self, env):
        while self.expr.eval(env) == AST.TRUE:
            self.block.eval(env)
