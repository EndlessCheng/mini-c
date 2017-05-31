# -*- coding:utf-8 -*-
from lexer import Lexer
from eparser import Parser
from eval import Eval

lex = Lexer('hello.e')
for i, token in enumerate(lex._read()):
    print token.image

ast = Parser(lex).program()
print ast
Eval(ast).eval()

# print '\'' in r'!"#$%&\'()*+,-./:;=<>?@[\]^_`{|}~'

