# -*- coding:utf-8 -*-
from eparser import ASList, ASTLeaf


class Eval:
    def __init__(self, ast):
        self.ast = ast

    def _eval(self):
        if isinstance(self.ast, ASTLeaf):
            return self.ast.value
        if isinstance(self.ast, ASList):
            if self.ast.is_unary_op():
                if self.ast.op == '-':
                    return - Eval(self.ast.right)._eval()
            if self.ast.is_binary_op():
                if self.ast.op == '+':
                    return Eval(self.ast.left)._eval() + Eval(self.ast.right)._eval()
                if self.ast.op == '-':
                    return Eval(self.ast.left)._eval() - Eval(self.ast.right)._eval()
                if self.ast.op == '*':
                    return Eval(self.ast.left)._eval() * Eval(self.ast.right)._eval()
                if self.ast.op == '/':
                    return Eval(self.ast.left)._eval() / Eval(self.ast.right)._eval()
        raise Exception("Eval error")

    def eval(self):
        for ast in self.ast.children:
            print Eval(ast)._eval()
