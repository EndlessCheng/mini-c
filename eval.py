# -*- coding:utf-8 -*-

from ast import AST, ASList, ASTLeaf


class Eval:
    def __init__(self, ast):
        self.ast = ast
