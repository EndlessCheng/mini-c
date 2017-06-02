# -*- coding:utf-8 -*-
from lexer import Lexer
from eparser import Parser
from environment import Environment

lex = Lexer('hello.e')
for i, token in enumerate(lex._read()):
    print token.image

ast = Parser(lex).program()
print ast

ast.eval(Environment())

# print '\'' in r'!"#$%&\'()*+,-./:;=<>?@[\]^_`{|}~'
