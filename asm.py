import sys
import os
import os.path
import re
from typing import *
from utils.console import console

from asm import lexer
from asm import tparser
from asm import compiler


def main():
    if len(sys.argv) < 3:
        exit('asm args error')

    filename = sys.argv[1]
    output   = sys.argv[2]

    if len(sys.argv) != 3: 
        exit(f"Usage: {sys.argv[0]} [filename]")

    with open(filename, 'r') as sourcecode:
        code = sourcecode.read()

    if not os.path.exists(filename):
        console.error(f"file '{filename}' does not exist")

    lex    = lexer.Lexer(code)
    parser = tparser.Parser(lex, filename)
    ast    = parser.parse()
    
    assembler = compiler.Compiler(ast)
    assembler.compile()

if __name__ == '__main__':
    main()

