# -*- coding:utf-8 -*-
import re
import itertools


class Lexer:
    _pattern = re.compile(
        r'\s*((//.*)|([0-9]+)|("(\\"|\\\\|\\n|[^"])*")|([A-Z_a-z][A-Z_a-z0-9]*'
        r'|==|<=|>=|&&|\|\||[!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~]))?')

    def __init__(self, fl):
        self.file = fl
        with open(fl) as f:
            self.lines = f.readlines()
        self.r = self._read()

    def _read(self):
        for line_no, line in enumerate(self.lines, 1):
            for match in self._pattern.findall(line):
                # print match
                if match[0] != '' and match[1] == '':
                    yield Token(line_no, *match)
            yield Token(line_no, image=r'\n')
        yield Token(-1)

    def peek(self):
        token = self.r.next()
        self.r = itertools.chain([token], self.r)
        return token

    def read(self):
        return self.r.next()


class Token:
    # FIXME: tmp?
    def __init__(self, line_no, image='', commit_image='', value_image='', str_image='', tmp='', id_image=''):
        self.line_no = line_no
        self.image = image
        self.value = int(value_image) if value_image != '' else None
        self.str = str_image.replace(r'\"', '"').replace(r'\\', '\\').replace(r'\n', '\n')[1:-1] if str_image != '' else None
        self.id = id_image if id_image != '' else None
