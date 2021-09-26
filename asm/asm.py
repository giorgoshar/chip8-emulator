import sys
import os
import os.path
import re
from typing  import *
from lexer   import *
from tparser import *

args = sys.argv[1:]
if len(args) <= 0:
    exit('USAGE AAAA')

filename = ''.join(args[0].split('.')[:-1])
with open(f'./{filename}.asm', 'r') as sourcecode:
    code = sourcecode.read()

lexer  = Lexer()
tokens = lexer.tokenize(code)

parser = Parser(filename, code)
binary = parser.parse(tokens)

with open(f'./{filename}.o', 'wb') as fp:
    fp.write(binary)

print(f'[DONE] bin:{filename}, size:{len(binary)}bytes',)