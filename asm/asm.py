import sys
import os
import os.path
import re

class Token:
    def __init__(self, kind: str, value: str, location: dict):
        self.kind   = kind
        self.value  = value
        self.loc    = location
    def __str__(self):
        return f'{self.kind:15} {self.value:<15} Location:{self.loc}'.replace('\n', '\\n')

class Tokenizer:
    keywords   = {'jmp', 'call', 'load', 'cls', 'draw', 'add', 'se', 'rand', 'sne', 'call', 'ret'}
    def __init__(self):
        self.tokens = []
    # https://docs.python.org/3/library/re.html#writing-a-tokenizer
    def tokenize(self, code: str) -> None:
        token_specification = [
            ('NUMBER',   r'0[xX][0-9a-fA-F]+|[0-9]+'),        # Integer or decimal number
            ('STRING',   r'\".*\"'),             # Match string inside quotation and ""
            ('REGISTER', r'[v|V]([0-9a-fA-F])'), # Match v1-vf registers
            ('REG_I',    r'\[I\]'),              # match `i` register
            ('LABEL',    r'[A-Za-z_]+\:'),       # Match Labels
            ('ID',       r'[A-Za-z_]+'),         # Identifiers
            ('OP',       r'[+\-*/]'),            # Arithmetic operators
            ('NEWLINE',  r'\n'),                 # Line endings
            ('SKIP',     r'[ \t]+'),             # Skip over spaces and tabs
            ('DIRECTIVE',r'\.[A-Za-z0-9]+'),     # Match directive
            ('COMMA',    r'\,'),                 # Match comma
            ('COMMENT',  r';.*'),               # Match comments
            ('MISMATCH', r'.'),                  # Any other character
        ]
        tok_regex  = '|'.join(r'(?P<%s>%s)' % pair for pair in token_specification)
        line_num   = 1
        line_start = 0
        for mo in re.finditer(tok_regex, code):

            kind     = mo.lastgroup
            value    = mo.group()
            column   = mo.start() - line_start
            location = { 'lineno': line_num, 'index' : column}

            if kind == 'NUMBER':
                self.tokens.append(Token(kind, value, location))
            elif kind == 'STRING':
                self.tokens.append(Token(kind, value, location))
            elif kind == 'ID' and value in self.keywords:
                kind = value.upper()
                self.tokens.append(Token(kind, value, location))
            elif kind == 'ID' and value not in self.keywords:
                self.tokens.append(Token(kind, value, location))
            elif kind == 'OP':
                self.tokens.append(Token(kind, value, location))
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
            elif kind == 'LABEL':
                self.tokens.append(Token(kind, value[:-1], location))
            elif kind == 'DIRECTIVE':
                self.tokens.append(Token(kind, value[1:], location))
            elif kind == 'REGISTER':
                self.tokens.append(Token(kind, value[1:], location))
            elif kind == 'REG_I':
                self.tokens.append(Token(kind, value, location))
            elif kind in ['SKIP', 'COMMA', 'COMMENT']:
                continue
            elif kind == 'MISMATCH':
                exit(f'unexpected `{value!r}` on line {line_num}')

        self.tokens.append(Token('EOF', '\0', location))

    def __iter__(self):
        return iter(self.tokens)

class Parser:
    def __init__(self):
        self.tokens  = []
        self.labels  = []
        self.binary  = bytearray()

    def parse(self, tokens: list) -> bytearray:
        self.tokens = iter(tokens)
        self.resolve_labels(tokens)

        # iter_token = iter(self.tokens)
        for tok in self.tokens:
            if tok.kind == 'DIRECTIVE':
                if tok.value == 'ascii':
                    tok = next(self.tokens)
                    if tok.kind != 'STRING':
                        self.excepted('STRING', tok)
                    for i in range(1, len(tok.value) - 1):
                        self.binary.append(ord(tok.value[i]))
                
                elif tok.value == 'font':
                    tok = next(self.tokens)
                    if tok.kind != 'ID':
                        self.excepted('ID', tok)

                    for i in range(0, 5):
                        tok   = next(self.tokens)
                        font  = tok.value.replace('"', '')
                        bfont = ''
                        for c in font:
                            if   c == ' ': bfont += '0'
                            elif c == '*': bfont += '1'
                            else: exit('font is wrong beeee')
                        self.binary.extend([int(bfont, 2) & 0xff])
                    
                    # while True:
                    #     tok = next(self.tokens)
                    #     if tok.kind != 'STRING':
                    #         break
                    #     font  = tok.value.replace('"', '')
                    #     bfont = ''
                    #     for c in font:
                    #         if   c == ' ': bfont += '0'
                    #         elif c == '*': bfont += '1'
                    #         else: exit('font is wrong beeee')
                    #     self.binary.extend([int(bfont, 2) & 0xff])
                elif tok.value == 'org':
                    next(self.tokens)
                else: self.unknown(tok)

            elif tok.kind == 'JMP':
                tok = next(self.tokens)
                if tok.kind != 'ID':
                    self.excepted('ID', tok)
                
                if tok.value not in [symbol[0] for symbol in self.labels]:
                    exit('could not find symbol ' + tok.value + ' in labels')
                
                addr = None
                for sym in self.labels:
                    if sym[0] == tok.value:
                        addr = sym[1]
                if addr == None:
                    exit('could not find symbol')
                opcode = self.jmp(addr)
                self.binary.extend(opcode)
            
            elif tok.kind == 'LOAD':
                tok = next(self.tokens)
                if tok.kind == 'REGISTER':
                    reg_x = int(tok.value)
                    tok = next(self.tokens)
                    if tok.kind == 'NUMBER':
                        reg_y = self.parse_number(tok.value)
                        opcode = (0x6000 | (reg_x << 8) | ( reg_y & 0x00ff)).to_bytes(2, 'big')
                        
                        self.binary.extend(opcode)
                elif tok.kind == 'REG_I':
                    tok = next(self.tokens)
                    if tok.kind == 'ID':
                        sym = None
                        for s in self.labels:
                            if s[0] == tok.value:
                                sym = s

                        if sym == None:
                            exit('Could not find identifier: ' + tok.value)
                        addr = int(sym[1]) & 0xfff
                    elif tok.kind == 'NUMBER':
                        addr = self.parse_number(tok.value) & 0xfff
                    elif tok.kind == 'REGISTER':
                        reg_x  = int(tok.value) & 0xf
                        opcode = (0xF055 | (reg_x << 8)).to_bytes(2, 'big')
                        self.binary.extend(opcode)
                        continue
                    else: self.excepted('ID, NUMBER, REGISTER', tok)

                    opcode = (0xA000 | addr).to_bytes(2, 'big')
                    self.binary.extend(opcode)
                else: self.excepted('REGISTER, REG_I', tok)

            elif tok.kind == 'DRAW':
                tok = next(self.tokens)
                if tok.kind != 'REGISTER':
                    exit ('draw excepted register as 1st argument but got' + tok.kind)
                arg1 = int(tok.value)

                tok = next(self.tokens)
                if tok.kind != 'REGISTER':
                    exit ('draw excepted register as 2nd argument but got' + tok.kind)
                arg2 = int(tok.value)

                tok = next(self.tokens)
                if tok.kind != 'NUMBER' and tok.value > 0xf:
                    exit ('draw excepted number as 3rd argument but got' + tok.kind)
                arg3 = self.parse_number(tok.value)

                opcode = self.draw(arg1, arg2, arg3)
                self.binary.extend(opcode)

            elif tok.kind == 'ADD':
                tok = next(self.tokens)
                if   tok.kind == 'REGISTER':
                    reg_x = self.parse_number(tok.value)

                    tok = next(self.tokens)
                    if tok.kind == 'NUMBER':
                        byte = self.parse_number(tok.value)
                        opcode = 0x7000 | (reg_x << 8) | (0x00ff & byte)
                        self.binary.extend(opcode.to_bytes(2, 'big'))
                    elif tok.kind == 'REGISTER':
                        reg_y = self.parse_number(tok.value)
                        opcode = 0x8004 | (reg_x << 8) | (reg_y << 4)
                        self.binary.extend(opcode.to_bytes(2, 'big'))
                    else:
                        self.excepted('NUMBER, REGISTER', tok)
                elif tok.kind == 'REG_I':
                    tok = next(self.tokens)
                    if tok.kind != 'REGISTER':
                        self.excepted('REGISTER', tok)
                    reg_x  = self.parse_number(tok.value) & 0xf
                    opcode = 0xF01E | (reg_x << 8)
                    self.binary.extend(opcode.to_bytes(2, 'big'))
                else: self.expected('REGISTER, REG_I', tok)
            
            elif tok.kind == 'CLS':
                self.binary.extend(0x00E0.to_bytes(2, 'big'))
            
            elif tok.kind == 'LABEL':
                pass
            
            elif tok.kind == 'SE':
                
                tok = next(self.tokens)
                if tok.kind != 'REGISTER':
                    self.excepted('REGISTER', tok)
                reg_x = self.parse_register(tok.value)

                tok = next(self.tokens)
                if tok.kind == 'REGISTER':
                    reg_y = self.parse_register(tok.value)
                    opcode = 0x5000 | (reg_x << 8) |  ( reg_y << 4)
                elif tok.kind == 'NUMBER':
                    number = self.parse_number(tok.value)
                    opcode = 0x3000 | (reg_x << 8) |  ( number & 0x00ff)
                else:
                    self.excepted('REGISTER, NUMBER', tok)
                self.binary.extend(opcode.to_bytes(2, 'big'))

            elif tok.kind == 'SNE':
                tok = next(self.tokens)
                if tok.kind != 'REGISTER':
                    self.excepted('REGISTER', tok)
                reg_x = self.parse_register(tok.value)

                tok = next(self.tokens)
                if tok.kind == 'REGISTER':
                    reg_y = self.parse_register(tok.value)
                    opcode = 0x9000 | (reg_x << 8) |  ( reg_y << 4)
                elif tok.kind == 'NUMBER':
                    number = self.parse_number(tok.value)
                    opcode = 0x4000 | (reg_x << 8) |  ( number & 0x00ff)
                else:
                    self.excepted('REGISTER, NUMBER', tok)
                self.binary.extend(opcode.to_bytes(2, 'big'))

            elif tok.kind == 'RAND':
                # Cxkk - RND Vx, byte
                tok = next(self.tokens)
                if tok.kind != 'REGISTER':
                    self.excepted('REGISTER', tok)
                reg_x = self.parse_number(tok.value)

                tok = next(self.tokens)
                if tok.kind != 'NUMBER':
                    self.excepted('NUMBER', tok)
                byte = self.parse_number(tok.value)

                self.binary.extend((0xC000 | (reg_x  << 8) | (0x00ff & byte)).to_bytes(2, 'big'))

            elif tok.kind == 'CALL':
                tok = next(self.tokens)
                if tok.kind not in ['ID']:
                    exit('excepted id but got type of ' + tok.kind)
                
                if tok.value not in [symbol[0] for symbol in self.labels]:
                    exit('could not find symbol ' + tok.value + ' in labels')
                
                addr = None
                for sym in self.labels:
                    if sym[0] == tok.value:
                        addr = sym[1]
                if addr == None:
                    exit('could not find symbol')
                opcode = self.call(addr)
                self.binary.extend(opcode)

            elif tok.kind == 'RET':
                self.binary.extend(0x00EE.to_bytes(2, 'big'))

            elif tok.kind == 'EOF':
                break

            else: exit(f'Could not parse {tok.kind}: {tok.value} at line:{tok.loc["lineno"]}')

        if tok.kind != 'EOF':
            self.excepted('EOF', tok)

        return self.binary

    def resolve_labels(self, tokens: list) -> list:
        pc = 0x200
        index  = 0

        while index < len(tokens):
            tok = tokens[index]
            if tok.kind == 'LABEL':
                if tok.value in [l[0] for l in self.labels]:
                    exit(f'LABEL already defined in: {self.find_label(tok.value)}')
                self.labels.append((tok.value, int(pc) & 0xfff))
            # instruction line
            elif tok.kind.upper() in [keyword.upper() for keyword in Tokenizer.keywords]:
                pc += 2
            elif tok.kind == 'DIRECTIVE':
                if tok.value == 'ascii':
                    index += 1
                    tok = tokens[index]
                    if tok.kind != 'STRING':
                        self.excepted(f'STRING', tok)
                    pc += len(tok.value) - 2  # remove quotation ""
                
                elif tok.value == 'org':
                    index += 1
                    tok = tokens[index]
                    if tok.kind != 'NUMBER':
                        self.excepted('NUMBER', tok)
                    pc = self.parse_number(tok.value)
                
                elif tok.value == 'font':
                    index += 1
                    tok = tokens[index]

                    if tok.value in [l[0] for l in self.labels]:
                        exit(f'LABEL already defined in: {self.find_label(tok.value)}')

                    self.labels.append((tok.value, int(pc) & 0xfff))
                    pc += 5
                else:
                    exit(f'Unexpected {tok}')
            index += 1
    def find_label(self, name):
        for sym in self.labels:
            if sym[0] == name:
                return sym
        exit('unreachable')
    
    def parse_number(self, value: str) -> int:
        if value[0:2] == '0x':
            return int(value, 16)
        return int(value)
    def parse_register(self, value: str) -> int:
        return int(value) & 0xf
    
    def call(self, addr):
        opcode = 0x2000 | (addr & 0x0FFF)
        return opcode.to_bytes(2, 'big')
    def jmp(self, addr):
        opcode = 0x1000 | (addr & 0x0FFF)
        return opcode.to_bytes(2, 'big')
    def draw(self, x, y, nibble):
        opcode = 0xD000 | (x << 8) | (y << 4) | (nibble & 0x000f)
        return opcode.to_bytes(2, 'big')
    def load(self, operand1, operand2):
        pass
    def se(self, register, number):
        pass
    
    def excepted(self, excepted: str, got: Token):
        raise Exception(f"Expected token {excepted} but got {got.kind} at line: { got.loc['lineno'] }")
    def unknown(self, tok: Token):
        raise Exception(f"Unkown {tok.kind}: `{tok.value}` at line:{ tok.loc['lineno'] }")


args = sys.argv[1:]
if len(args) <= 0:
    exit('USAGE AAAA')

filename = ''.join(args[0].split('.')[:-1])
with open(f'./{filename}.asm', 'r') as sourcecode:
    code = sourcecode.read()

tokenizer = Tokenizer()
tokenizer.tokenize(code)

parser = Parser()
parser.parse(tokenizer.tokens)

with open(f'./{filename}.o', 'wb') as fp:
    fp.write(parser.binary)

print(f'[DONE] bin:{filename}, size:{len(parser.binary)}bytes',)