# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=unused-import
# pylint: disable=no-self-use

import sys
import os
import os.path
import re
import struct

os.system("clear")

REGEX_TRAIL_WHITESPACES_END   = r'[ \t]+$'
REGEX_TRAIL_WHITESPACES_BEGIN = r'^\s+'
REGEX_COMMENT  = r';[^;]*$'
REGEX_LABEL    = r'\.(?P<label>[a-zA-Z_][a-zA-Z_0-9]*)'
REGEX_ADDR     = r'0[xX]([0-9a-fA-F]{3})'
REGEX_BYTE     = r'0[xX]([0-9a-fA-F]{2})'
REGEX_NIBBLE   = r'0[xX]([0-9a-fA-F])'
REGEX_REG      = r'V([0-9a-fA-F])'
REGEX_JMP_CALL = r'(JMP|CALL)'

class Tokenizer:
    def __init__(self, kind, value):
        self.kind  = kind
        self.value = value

class Parser:
    def __init__(self):
        self.lineIndex = 0
        self.tokens = []
    
    def parse(self, text):
        
        token = text.split()
        
        if token[0].strip() == 'ADD' and len(token) == 3:
            args = []
            if re.match(REGEX_REG, token[1]):
                arg1 = Tokenizer('REG', self.extract_reg(token[1]))
                args.append(arg1)

            if self.is_number(int(token[2])):
                arg2 = Tokenizer('NUMBER', int(token[2]))
                args.append(arg2)

            ins = Tokenizer('ADD', args)
            self.tokens.append(ins)


        if token[0].strip() == 'LD' and len(token) == 3:
            args = []
            if re.match(REGEX_REG, token[1]):
                arg1 = Tokenizer('REG', self.extract_reg(token[1]))
                args.append(arg1)

            if token[1].strip() == 'I':
                arg1 = Tokenizer('INDEX', token[1])
                args.append(arg1)


            if self.is_number(token[2]):
                arg2 = Tokenizer('NUMBER', int(token[2]))
                args.append(arg2)

            if re.match(REGEX_REG, token[2]):
                arg2 = Tokenizer('REG', self.extract_reg(token[1]))
                args.append(arg2)


            ins = Tokenizer('LD', args)
            self.tokens.append(ins)


    def extract_reg(self, REG):
        reg = REG.replace('V', '')
        if not reg.isdigit():
            self.throw_syntax_error(f'Execpted `Vx` found `{REG}`') 
        return int(reg)

    def is_number(self, n):
        return isinstance(n, int) or n.isdigit()

    def throw_syntax_error(self,  message):
        sys.exit(f'{message} at line: {self.lineIndex}')

parser = Parser()
# with open('./SOURCES/MAZE.SRC', 'r') as fp:
# with open('./SOURCES/UFO.SRC', 'r') as fp:
with open('./test.asm', 'r') as fp:
    for idx, line in enumerate(fp):
        parser.lineIndex = idx + 1
        # remove end of line
        line = line.rstrip()

        # remove comment in the line
        line = re.sub(REGEX_COMMENT, '', line)

        # remove whitespaces at the begging and in then of the line
        line = re.sub(REGEX_TRAIL_WHITESPACES_BEGIN, '', line)
        line = re.sub(REGEX_TRAIL_WHITESPACES_END,   '', line)

        # remove commas
        line = re.sub(r',', '', line)

        # skip if line is empy or starts with symbol
        if len(line) == 0:
            continue

        line = line.upper()
        if 'OPTION' in line\
        or 'ALIGN'  in line: 
            continue

        parser.parse(line)

    for idx, token in enumerate(parser.tokens):
        print(token.kind, token.value)
        if isinstance(token.value, list):
            for child_token in token.value:
                print('   ', child_token.kind, child_token.value)

