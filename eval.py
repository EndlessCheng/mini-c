# -*- coding:utf-8 -*-
from eparser import ASList, ASTLeaf


class Eval:
    def __init__(self, ast):
        self.ast = ast

    def eval(self):
        if isinstance(self.ast, ASTLeaf):
            return self.ast.value
        if isinstance(self.ast, ASList):
            if self.ast.op == '+':
                return Eval(self.ast.left).eval() + Eval(self.ast.right).eval()
            if self.ast.op == '-':
                return Eval(self.ast.left).eval() - Eval(self.ast.right).eval()
            if self.ast.op == '*':
                return Eval(self.ast.left).eval() * Eval(self.ast.right).eval()
            if self.ast.op == '/':
                return Eval(self.ast.left).eval() / Eval(self.ast.right).eval()
