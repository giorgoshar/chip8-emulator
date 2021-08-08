import sys
import os
import os.path
import re
'''
    TODO: 
        change endfont to DIRECTIVE
        adding line number in label list 
'''

class SyntaxError(Exception): pass
class Undefined(Exception):   pass
class Unreachable(Exception): pass
class NotImplemented(Exception): pass

class Token:
    def __init__(self, kind: str, value: str, location: dict):
        self.kind   = kind
        self.value  = value
        self.loc    = location
    def __str__(self):
        return f'{self.kind:15} {self.value:<15} Location:{self.loc}'.replace('\n', '\\n')

class Tokenizer:
    keywords   = {'jmp', 'load', 'cls', 'draw', 'add', 'rand', 'se', 'sne', 'call', 'ret', 'skp', 'sknp'}
    def __init__(self):
        self.tokens = []
    # https://docs.python.org/3/library/re.html#writing-a-tokenizer
    def tokenize(self, code: str) -> None:
        token_specification = [
            ('NUMBER',   r'0[xX][0-9a-fA-F]+|[0-9]+'),        # Integer or decimal number
            ('STRING',   r'\".*\"'),             # Match string inside quotation and ""
            ('REGISTER', r'[v|V]([0-9a-fA-F]+)'), # Match v1-vf registers
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
        return self.tokens

    def __iter__(self):
        return iter(self.tokens)

class Parser:
    def __init__(self):
        self.tokens  = []
        self.labels  = []
        self.binary  = bytearray()
        self.tokidx  = 0

    def parse(self, tokens: list) -> bytearray:
        self.resolve_labels(tokens)

        self.tokens = iter(tokens)
        for tok in self.tokens:
            
            if tok.kind == 'DIRECTIVE':
                if tok.value == 'ascii':
                    tok = next(self.tokens)
                    self.expected(['STRING'], tok)
                    for i in range(1, len(tok.value) - 1):
                        self.binary.append(ord(tok.value[i]))

                elif tok.value == 'font':
                    tok = next(self.tokens)
                    self.expected(['ID'], tok)
                    
                    while True:
                        tok = next(self.tokens)
                        if (tok.kind == 'ID') and (tok.value == 'endfont'):
                            break
                        self.expected(['NUMBER'], tok)
                        bfont = self.parse_number(tok.value)
                        self.binary.extend([bfont])
                    self.expected(['ID'], tok) # expect ID: endfont
                elif tok.value == 'inc':
                    next(self.tokens)
                    raise NotImplemented(tok)
                elif tok.value == 'org':
                    next(self.tokens)
                elif tok.value == 'var':
                    next(self.tokens) # skip ID
                    tok = next(self.tokens)
                    self.expected(['NUMBER'], tok)
                    number = self.parse_number(tok.value)
                    self.binary.extend(number.to_bytes(2, 'big'))
                else: self.unknown(tok)

            elif tok.kind == 'JMP':
                tok = next(self.tokens)
                self.expected(['ID'], tok)
                label = self.find_label(tok)
                addr  = self.parse_number(label[1]) & 0xfff
                self.jmp(addr)
            
            elif tok.kind == 'LOAD':
                tok = next(self.tokens)
                self.expected(['REGISTER', 'REG_I'], tok)
                if tok.kind == 'REGISTER':
                    Vx  = self.parse_register(tok.value)
                    tok = next(self.tokens)
                    self.expected(['NUMBER', 'REG_I'], tok)
                    if tok.kind == 'NUMBER':
                        Vy = self.parse_number(tok.value)
                        opcode = (0x6000 | (Vx << 8) | ( Vy & 0x00ff)).to_bytes(2, 'big')
                        self.binary.extend(opcode)
                    elif tok.kind == 'REG_I':
                        opcode = (0xF065  | (Vx << 8)).to_bytes(2, 'big')
                        self.binary.extend(opcode)
                elif tok.kind == 'REG_I':
                    tok = next(self.tokens)
                    self.expected(['ID', 'NUMBER', 'REGISTER'], tok)
                    
                    if tok.kind == 'ID':
                        label = self.find_label(tok)
                        addr  = self.parse_number(label[1]) & 0xfff
                        opcode = (0xA000 | addr).to_bytes(2, 'big')
                    elif tok.kind == 'NUMBER':
                        addr = self.parse_number(tok.value) & 0xfff
                        opcode = (0xA000 | addr).to_bytes(2, 'big')
                    elif tok.kind == 'REGISTER':
                        reg_x  = int(tok.value) & 0xf
                        opcode = (0xF055 | (reg_x << 8)).to_bytes(2, 'big')
                    self.binary.extend(opcode)

            elif tok.kind == 'DRAW':
                tok = next(self.tokens)
                self.expected(['REGISTER'], tok)
                arg1 = self.parse_register(tok.value)

                tok = next(self.tokens)
                self.expected(['REGISTER'], tok)
                arg2 = self.parse_register(tok.value)

                tok = next(self.tokens)
                self.expected(['NUMBER'], tok)
                nibble = self.parse_number(tok.value)
                if nibble > 0xf:
                    self.expected(['NUMBER'], tok)
                arg3 = self.parse_number(tok.value)

                self.draw(arg1, arg2, arg3)

            elif tok.kind == 'ADD':
                tok = next(self.tokens)
                self.expected(['REGISTER', 'REG_I'], tok)

                if tok.kind == 'REGISTER':
                    Vx = self.parse_number(tok.value)

                    tok = next(self.tokens)
                    self.expected(['NUMBER', 'REGISTER'], tok)

                    if tok.kind == 'NUMBER':
                        byte = self.parse_number(tok.value)
                        opcode = 0x7000 | (Vx << 8) | (0x00ff & byte)
                    elif tok.kind == 'REGISTER':
                        Vy = self.parse_number(tok.value)
                        opcode = 0x8004 | (Vx << 8) | (Vy << 4)
                elif tok.kind == 'REG_I':
                    tok = next(self.tokens)
                    self.expected(['REGISTER'], tok)

                    Vx  = self.parse_register(tok.value) & 0xf
                    opcode = 0xF01E | (Vx << 8)

                self.binary.extend(opcode.to_bytes(2, 'big'))

            elif tok.kind == 'CLS':
                self.binary.extend(0x00E0.to_bytes(2, 'big'))
            
            elif tok.kind == 'LABEL':
                pass
            
            elif tok.kind == 'SE':
                
                tok = next(self.tokens)
                self.expected(['REGISTER'], tok)
                Vx = self.parse_register(tok.value)

                tok = next(self.tokens)
                self.expected(['REGISTER', 'NUMBER'], tok)

                if tok.kind == 'REGISTER':
                    Vy = self.parse_register(tok.value)
                    opcode = 0x5000 | (Vx << 8) |  ( Vy << 4)
                elif tok.kind == 'NUMBER':
                    number = self.parse_number(tok.value)
                    opcode = 0x3000 | (Vx << 8) |  ( number & 0x00ff)
                self.binary.extend(opcode.to_bytes(2, 'big'))
            elif tok.kind == 'SNE':
                
                tok = next(self.tokens)
                self.expected(['REGISTER'], tok)
                Vx = self.parse_register(tok.value)

                tok = next(self.tokens)
                self.expected(['REGISTER', 'NUMBER'], tok)

                if tok.kind == 'REGISTER':
                    Vy = self.parse_register(tok.value)
                    opcode = 0x9000 | (Vx << 8) |  ( Vy << 4)
                elif tok.kind == 'NUMBER':
                    number = self.parse_number(tok.value)
                    opcode = 0x4000 | (Vx << 8) |  ( number & 0x00ff)                
                
                self.binary.extend(opcode.to_bytes(2, 'big'))

            elif tok.kind == 'SKP':
                tok = next(self.tokens)
                self.expected(['NUMBER'], tok)
                key = self.parse_number(tok.value) & 0xf
                opcode = (0xE09E | (key << 8))
                self.binary.extend(opcode.to_bytes(2, 'big'))
            elif tok.kind == 'SKNP':
                tok = next(self.tokens)
                self.expected(['NUMBER'], tok)
                key = self.parse_number(tok.value) & 0xf
                opcode = (0xE0A1 | (key << 8))
                self.binary.extend(opcode.to_bytes(2, 'big'))
            
            elif tok.kind == 'RAND':

                tok = next(self.tokens)
                self.expected(['REGISTER'], tok)
                Vx = self.parse_number(tok.value)

                tok = next(self.tokens)
                self.expected(['NUMBER'], tok)
                byte = self.parse_number(tok.value)

                self.binary.extend((0xC000 | (Vx  << 8) | (0x00ff & byte)).to_bytes(2, 'big'))

            elif tok.kind == 'CALL':
                tok = next(self.tokens)
                self.expected(['ID'], tok)

                label = self.find_label(tok)
                addr  = self.parse_number(label[1]) & 0xfff
                self.call(addr)
            elif tok.kind == 'RET':
                self.binary.extend(0x00EE.to_bytes(2, 'big'))

            elif tok.kind == 'EOF':
                break

            else: exit(f'Could not parse {tok.kind}: {tok.value} at line:{tok.loc["lineno"]}')

        self.expected(['EOF'], tok)
        return self.binary

    def peek(self):
        return self.tokens[ self.tokidx + 1 ]        
    def eat(self):
        self.tokidx += 1
        return self.tokens[ self.tokidx ]

    def tobinarray(self, opcode: int) -> bytearray:
        _bytes = opcode.to_bytes(2, 'big')
        return _bytes
    def addbinary(self, opcode: int) -> None:
        self.binary.extend(self.tobinarray(opcode))

    def resolve_labels(self, tokens: list) -> list:
        tokens_iter = iter(tokens)
        pc = 0x200
        for tok in tokens_iter:
            if tok.kind == 'LABEL':
                if tok.value in [l[0] for l in self.labels]:
                    raise SyntaxError(f'Label already defined at {self.find_label(tok.value)}')
                self.labels.append((tok.value, int(pc) & 0xfff))
            # instruction line
            elif tok.kind.upper() in [keyword.upper() for keyword in Tokenizer.keywords]:
                pc += 2
            elif tok.kind == 'DIRECTIVE':
                if tok.value == 'ascii':
                    tok = next(tokens_iter)
                    self.expected(['STRING'], tok)
                    pc += len(tok.value) - 2  # remove quotation ""
                
                elif tok.value == 'org':
                    tok = next(tokens_iter)
                    self.expected(['NUMBER'], tok)
                    pc = self.parse_number(tok.value)
                
                elif tok.value == 'font':
                    tok = next(tokens_iter)
                    if tok.value in [l[0] for l in self.labels]:
                        exit(f'LABEL already defined in: {self.find_label(tok.value)}')
                    self.labels.append((tok.value, int(pc) & 0xfff))
                    while True:
                        if (tok.kind == 'ID') and (tok.value == 'endfont'):
                            break
                        pc += 1
                        tok = next(tokens_iter)
                    # fix this
                    pc -= 1
                    self.expected(['ID'], tok)

                elif tok.value == 'var':
                    tok = next(tokens_iter)
                    self.expected(['ID'], tok)
                    identifier = tok.value

                    tok = next(tokens_iter)
                    self.expected(['NUMBER'], tok)
                    value = self.parse_number(tok.value)

                    self.labels.append((identifier, int(pc) & 0xfff))
                    pc += 2
    
    def find_label(self, tok):
        for label in self.labels:
            if label[0] == tok.value:
                return label
        raise Undefined(f"`{tok.value}` at line ???")
    
    def parse_number(self, value: str) -> int:
        if str(value)[0:2] == '0x':
            return int(value, 16)
        return int(value)
    def parse_register(self, value: str) -> int:
        if int(value, 16) > 0xf: exit('error parsing register')
        return int(value, 16) & 0xf
    
    def call(self, addr):
        opcode = (0x2000 | (addr & 0x0FFF)).to_bytes(2, 'big')
        self.binary.extend(opcode)
    def jmp(self, addr):
        opcode = (0x1000 | (addr & 0x0FFF)).to_bytes(2, 'big')
        self.binary.extend(opcode)
    def draw(self, x, y, nibble):
        opcode = (0xD000 | (x << 8) | (y << 4) | (nibble & 0x000f)).to_bytes(2, 'big')
        self.binary.extend(opcode)

    def expected(self, tokens, tok):
        if tok.kind not in tokens:
            raise SyntaxError(f"Expected {tokens} but got {tok.kind} at line: {tok.loc['lineno']}")
        return True

    def unknown(self, tok: Token):
        raise Undefined(f"{tok.kind}: `{tok.value}` at line:{ tok.loc['lineno'] }")


args = sys.argv[1:]
if len(args) <= 0:
    exit('USAGE AAAA')

filename = ''.join(args[0].split('.')[:-1])
with open(f'./{filename}.asm', 'r') as sourcecode:
    code = sourcecode.read()

tokenizer = Tokenizer()
tokens = tokenizer.tokenize(code)

parser = Parser()
parser.parse(tokens)

with open(f'./{filename}.o', 'wb') as fp:
    fp.write(parser.binary)

print(f'[DONE] bin:{filename}, size:{len(parser.binary)}bytes',)