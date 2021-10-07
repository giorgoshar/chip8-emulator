import sys
import os
import os.path
import re
from typing import *
from utils.console import console
from asm import lexer
from asm import tparser

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

lex = lexer.Lexer()
tokens = lex.tokenize(code)

parser = tparser.Parser(filename, code)
binary = parser.parse(tokens)

with open(output, 'wb') as fp:
    fp.write(binary)

fullpath = os.getcwd() + output
console.done(f"bin : {fullpath}")
console.done(f"size: {len(binary)}bytes")