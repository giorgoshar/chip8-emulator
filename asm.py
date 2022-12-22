import sys
import os
import os.path
from utils.console import console

from asm import lexer
from asm import tparser

if len(sys.argv) < 3:
    exit('asm args error')

filename = sys.argv[1]
output   = sys.argv[2]

if len(sys.argv) != 3: 
    exit(f"Usage: {sys.argv[0]} [filename]")

source = lexer.Source(filename)
lex    = lexer.Lexer(source)
tokens = lex.tokenize(source.code)

for token in tokens:
    print(token)

parser = tparser.Parser(filename)
binary = parser.parse(tokens)

with open(output, 'wb') as fp:
    fp.write(binary)

fullpath = os.getcwd() + output
console.info(f"bin : {fullpath}")
console.info(f"size: {len(binary)}bytes")