import sys
import os
import os.path
import re
from typing import *
from asm import lexer
from asm import tparser

if len(sys.argv) < 3:
    exit('asm args error')

filename = sys.argv[1]
output   = sys.argv[2]

if len(sys.argv) != 3: 
    exit(f"Usage: {sys.argv[0]} [filename]")

print(f"\033[0;32m[INFO]\033[0m Compiling: {filename}")

with open(filename, 'r') as sourcecode:
    code = sourcecode.read()

if not os.path.exists(filename):
    exit(f"\033[1;31m[ERROR]\033[0m file '{filename}' does not exist")


lex = lexer.Lexer()
tokens = lex.tokenize(code)

parser = tparser.Parser(filename, code)
binary = parser.parse(tokens)

with open(output, 'wb') as fp:
    fp.write(binary)

fullpath = os.getcwd() + output
# print(f'\033[0;32m[DONE]\033[0m bin : {fullpath}')
# print(f'\033[0;32m[DONE]\033[0m size: {len(binary)}bytes')