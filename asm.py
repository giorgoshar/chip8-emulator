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

os.system("clear")

REGEX_COMMENT = r';[^;]*$'
REGEX_TRAIL_WHITESPACES_END   = r'[ \t]+$'
REGEX_TRAIL_WHITESPACES_BEGIN = r'^\s+'

class Tokenizer:
    def __init__(self):
        self.instructions = {}
        self.labels = {}
        self.binary = bytearray()
        self.tokens = {
            'LD' : {
                'instr': 0x6000,
                'bytes': 2
            }
        }
        self.error = 0
        self.addr  = 0x0
        self.pc    = 0x200
    
    def parse(self, text):
        print(text)

    def is_instruction(self, tok):
        if tok in self.tokens:
            return True

    def is_label(self, tok):
        pass

    def is_option(self, tok):
        pass

    def parse_args(self, arg):
        pass

addr_counter = 0x0
binary = bytearray()

# with open('./SOURCES/MAZE.SRC', 'r') as fp:
with open('./SOURCES/UFO.SRC', 'r') as fp:
    print(f'{"cp":4} | {"line":32} | {"parsed":32} | {"opcode":<8} | bin')
    print(f'-' * 100)
    for line in fp:

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

        ins = line.split()
        # ins = [s.upper() for s in line]
        opcode = 0x0000
        str_opcode = ''

        if ins[0].upper() == 'OPTION': continue
        if ins[0].upper() == 'ALIGN' : continue

        if ins[0] == 'LD' and ins[1][0] == 'V' and ins[2][0] != 'V':

            if ins[2][0] == '#':
                ins[2] = ins[2].replace('#', '')

            instruction = 0x6000
            arg1 = int(ins[1][1:], 16)
            arg2 = int(ins[2], 16)
            opcode = instruction | (arg1 << 8) | (arg2 << 4)
            str_opcode = f'0x{instruction:x} 0x{arg1} 0x{arg2}'

        if ins[0] == 'RND' and ins[1][0] == 'V' and ins[2][0] != 'V':
            instruction = 0xc000
            arg1 = int(ins[1][1:], 16)
            arg2 = int(ins[2], 16)
            opcode = instruction | (arg1 << 8) | (arg2 & 0x00ff)
            str_opcode = f'0x{instruction:x} 0x{arg1} 0x{arg2}'

        if ins[0] == 'SE' and ins[1][0] == 'V' and ins[2][0] != 'V':
            instruction = 0x3000
            arg1 = int(ins[1][1:], 16)
            arg2 = int(ins[2], 16)
            opcode = instruction | (arg1 << 8) | (arg2 & 0x00ff)
            str_opcode = f'0x{instruction:x} 0x{arg1:<x} 0x{arg2:<x}'

        if ins[0] == 'ADD' and ins[1][0] == 'V' and ins[2][0] != 'V':
            instruction = 0x7000
            arg1 = int(ins[1][1:], 16)
            arg2 = int(ins[2], 16)
            opcode = instruction | (arg1 << 8) | (arg2 & 0x00ff)
            str_opcode = f'0x{instruction:x} 0x{arg1:<x} 0x{arg2:<x}'

        print(f'{addr_counter:04x} | {line:32} | {str(ins):32} | 0x{opcode:<6x} | {str_opcode}')

        addr_counter += 2

