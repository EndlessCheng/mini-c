# -*- coding:utf-8 -*-
from eparser import AST, ASList, ASTLeaf


class Eval:
    def __init__(self, ast):
        self.ast = ast

    def _eval(self):
        if isinstance(self.ast, ASTLeaf):
            return self.ast.value
        elif isinstance(self.ast, ASList):
            if self.ast.type == AST.PRINT:
                print Eval(self.ast.expr)._eval()
            elif self.ast.type == AST.UNARY:
                if self.ast.op == '-':
                    return - Eval(self.ast.right)._eval()
            elif self.ast.type == AST.BINARY:
                if self.ast.op == '+':
                    return Eval(self.ast.left)._eval() + Eval(self.ast.right)._eval()
                elif self.ast.op == '-':
                    return Eval(self.ast.left)._eval() - Eval(self.ast.right)._eval()
                elif self.ast.op == '*':
                    return Eval(self.ast.left)._eval() * Eval(self.ast.right)._eval()
                elif self.ast.op == '/':
                    return Eval(self.ast.left)._eval() / Eval(self.ast.right)._eval()
                elif self.ast.op == '==':
                    return Eval(self.ast.left)._eval() == Eval(self.ast.right)._eval()
                elif self.ast.op == '!=':
                    return Eval(self.ast.left)._eval() != Eval(self.ast.right)._eval()
            elif self.ast.type == AST.IF:
                if Eval(self.ast.expr)._eval():
                    Eval(self.ast.if_block)._eval()
                elif self.ast.else_block is not None:
                    Eval(self.ast.else_block)._eval()
            elif self.ast.type == AST.WHILE:
                while Eval(self.ast.expr)._eval():
                    Eval(self.ast.block)._eval()
        else:
            raise Exception("Eval error")

    def eval(self):
        for ast in self.ast.children:
            Eval(ast)._eval()
