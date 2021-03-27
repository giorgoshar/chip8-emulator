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

class Token:
    def __init__(self, value, kind, callback, args):
        self.value = value
        self.kind  = kind
        self.cb    = callback
        self.args  = args

class Parser:
    def __init__(self):
        self.binary = bytearray()
        self.tokens = {}
        self.error = 0
        self.addr  = 0x0
        self.pc    = 0x200
        self.index = 0
        
        self.types = [
            0x1, # LABEL
            0x2, # INSTRUCTION
        ]

        self.symbols = []
        self.labels  = []
        self.ins     = []
    
    def parse(self, text):
        
        token = text.split()

        # if self.is_label(token):
        #     pass
        opcode = None

        if (token[0] == 'ADD'
        and re.match(REGEX_REG, token[1])
        and self.is_number(int(token[2]))):
            arg1 = int(token[1][1:])
            arg2 = int(token[2])

            opcode = 0x7000 | (arg1) << 8 | arg2
            self.ins.append(opcode)

        if (token[0].strip() == 'LD'
        and re.match(REGEX_REG, token[1])
        and self.is_number(int(token[2]))):
            arg1 = int(token[1][1:])
            arg2 = int(token[2])
            
            opcode = 0x6000 | (arg1) << 8 | arg2
            self.ins.append(opcode)

        if (token[0].strip() == 'LD'
        and token[1].strip() == 'I'
        and self.is_number(int(token[2]))):
            arg2 = int(token[2][1:])

            opcode = 0xa000 | (arg2 & 0x0fff)
            self.ins.append(opcode)

        # if (token[0].strip() == 'LD'
        # and re.match(REGEX_REG, token[1])
        # and re.match(REGEX_REG, token[2])):
            
        #     arg1 = int(token[1][1:])
        #     arg2 = int(token[2][1:])
            
        #     opcode = 0xa000 | (arg2 & 0x0fff)
        #     self.ins.append(opcode)

        # self.index += 1

        if opcode: print(f'0x{opcode:<6x} -> {text}')

    def ins_jump(self, nnn):
        # 1nnn
        return 0x1000 | (nnn & 0x0fff)

    def is_instruction(self, tok):
        pass

    def is_label(self, token):
        sys.exit('_not_implemented_')
        if re.match(REGEX_JMP_CALL, token):
            return True
        return False

    def is_option(self, tok):
        pass

    def is_number(self, n):
        return isinstance(n, int)

    def parse_args(self, arg):
        pass

parser = Parser()
# s = parser.ins_jump(0x30)
# print(hex(s))
# sys.exit()
# with open('./SOURCES/MAZE.SRC', 'r') as fp:
# with open('./SOURCES/UFO.SRC', 'r') as fp:
with open('./test.asm', 'r') as fp:
    print(f'{"cp":4} | {"line":32} | {"parsed":32} | {"opcode":<8} | bin')
    print('-' * 100)
    for idx, line in enumerate(fp):

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


        # ins = line.split()
        # # ins = [s.upper() for s in line]
        # opcode     = 0x0000
        # str_opcode = ''
        
        # if ins[0].upper() == 'OPTION': continue
        # if ins[0].upper() == 'ALIGN' : continue

        
        # if ins[0] == 'LD' and ins[1][0] == 'V' and ins[2][0] != 'V':

        #     if ins[2][0] == '#':
        #         ins[2] = ins[2].replace('#', '')

        #     instruction = 0x6000
        #     arg1 = int(ins[1][1:], 16)
        #     arg2 = int(ins[2], 16)
        #     opcode = instruction | (arg1 << 8) | (arg2 << 4)
        #     str_opcode = f'0x{instruction:x} 0x{arg1} 0x{arg2}'

        # if ins[0] == 'RND' and ins[1][0] == 'V' and ins[2][0] != 'V':
        #     instruction = 0xc000
        #     arg1 = int(ins[1][1:], 16)
        #     arg2 = int(ins[2], 16)
        #     opcode = instruction | (arg1 << 8) | (arg2 & 0x00ff)
        #     str_opcode = f'0x{instruction:x} 0x{arg1} 0x{arg2}'

        # if ins[0] == 'SE' and ins[1][0] == 'V' and ins[2][0] != 'V':
        #     instruction = 0x3000
        #     arg1 = int(ins[1][1:], 16)
        #     arg2 = int(ins[2], 16)
        #     opcode = instruction | (arg1 << 8) | (arg2 & 0x00ff)
        #     str_opcode = f'0x{instruction:x} 0x{arg1:<x} 0x{arg2:<x}'

        # if ins[0] == 'ADD' and ins[1][0] == 'V' and ins[2][0] != 'V':
        #     instruction = 0x7000
        #     arg1 = int(ins[1][1:], 16)
        #     arg2 = int(ins[2], 16)
        #     opcode = instruction | (arg1 << 8) | (arg2 & 0x00ff)
        #     str_opcode = f'0x{instruction:x} 0x{arg1:<x} 0x{arg2:<x}'

        # print(f'{addr_counter:04x} | {line:32} | {str(ins):32} | 0x{opcode:<6x} | {str_opcode}')


# print(list(map(hex, parser.ins)))