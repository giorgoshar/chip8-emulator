import sys
import os
import os.path
import re
from typing import *
from utils.console import console

from asm import lexer
from asm import tparser

class Compiler:
    def __init__(self, _parser):
        self.parsed = _parser
        self.output = None

    def compile(self) -> bytearray or None:
        for token in self.parsed.tokens:
            print('Compile:' , token)
            exit('aaaaaaaaaaaaaaaaaa')
        return self.output

if len(sys.argv) < 3:
    exit('asm args error')

filename = sys.argv[1]
output   = sys.argv[2]

if len(sys.argv) != 3: 
    exit(f"Usage: {sys.argv[0]} [filename]")

console.info(f"Compiling: {filename}")

with open(filename, 'r') as sourcecode:
    code = sourcecode.read()

if not os.path.exists(filename):
    console.error(f"file '{filename}' does not exist")

lex = lexer.Lexer(code)
parser = tparser.Parser(lex, filename)
binary = parser.parse()

print('Binary:', binary)
# compiler = Compiler(parser)
# compiler.compile()

with open(output, 'wb') as fp:
    fp.write(binary)

fullpath = os.getcwd() + output
console.info(f"bin : {fullpath}")
console.info(f"size: {len(binary)}bytes")
