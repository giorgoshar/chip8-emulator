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
        self.lineIndex  = 0
        self.tokenIndex = 0
        self.tokens     = []
    
    def parse(self, text):
        
        token = text.split()

        for tok in token:
            if tok.strip() == 'ADD':
                ins = Tokenizer('INSTRUCTION', 'ADD')
                self.tokens.append(ins)

            if tok.strip() == 'LD':
                ins = Tokenizer('INSTRUCTION', 'LD')
                self.tokens.append(ins)

            if re.match(REGEX_REG, tok):
                reg = Tokenizer('REG', self.extract_reg(tok))
                self.tokens.append(reg)

            if self.is_number(tok):
                num = Tokenizer('NUMBER', int(tok))
                self.tokens.append(num)

            if tok.strip() == 'I':
                index = Tokenizer('INDEX', tok)
                self.tokens.append(index)



    def extract_reg(self, REG):
        reg = REG.replace('V', '')
        if not reg.isdigit():
            self.throw_syntax_error(f'Execpted `Vx` found `{REG}`') 
        return int(reg)

    def is_number(self, n):
        return n.isdigit()

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
