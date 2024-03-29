import sys
sys.path.append('C:\\Users\\User\\Desktop\\Giorgos\\Dev\\emulators\\chip8')
from typing        import Iterator
from utils.console import console
from asm.lexer     import *

def to_bytes(value: int):
    if type(value) is not int:
        console.error('Value must be an integer')
    return value.to_bytes(2, 'big')

class Parser:
    def __init__(self, filename: str):
        self.filename :str             = filename
        self.tokens   :Iterator[Token] = iter([])
        self.labels   :list[Label]     = []
        self.binary   :bytearray       = bytearray()

    def parse(self, tokens: list[Token]) -> bytearray:
        self.parse_labels(tokens)
        self.resolve_alias(tokens)
        self.tokens = iter(tokens)
        for tok in self.tokens:
            if   tok.kind == TokenKind.DIRECTIVE:
                if   tok.value == 'ascii':
                    tok = next(self.tokens)
                    self.expected([TokenKind.STRING], tok)
                    output = self.parse_ascii(tok.value)
                    self.binary.extend(output)
                elif tok.value == 'font':
                    tok = next(self.tokens)
                    self.expected([TokenKind.IDENTIFIER], tok)
                    # identifier = tok.value
                    font_bytes = bytearray()
                    while True:
                        tok = next(self.tokens)
                        if tok.value == 'endfont': break
                        self.expected([TokenKind.NUMBER], tok)
                        font_bytes.append(self.parse_number(tok.value))
                    self.binary.extend(bytearray(font_bytes))
                    self.expected([TokenKind.IDENTIFIER], tok)
                elif tok.value == 'inc':
                    tok = next(self.tokens)
                    self.expected([TokenKind.STRING], tok)
                elif tok.value == 'org':
                    next(self.tokens)
                elif tok.value == 'byte':
                    next(self.tokens) # skip ID
                    tok = next(self.tokens)
                    self.expected([TokenKind.NUMBER], tok)
                    number = self.parse_number(tok.value)
                    self.binary.extend(to_bytes(number))
                else: self.undefined(tok)
            elif tok.kind == TokenKind.INSTRUCTION:

                if   tok.value == InstrKind.CLS:
                    self.binary.extend(to_bytes(0x00E0))
                elif tok.value == InstrKind.JMP:
                    tok = next(self.tokens)
                    self.expected([TokenKind.IDENTIFIER, TokenKind.NUMBER], tok)

                    if tok.kind == TokenKind.IDENTIFIER:
                        label = self.find_label(tok)
                        addr  = self.parse_number(label.addr)
                    if tok.kind == TokenKind.NUMBER:
                        addr = self.parse_number(tok.value)
                    self.jmp(addr)

                elif tok.value == InstrKind.LOAD:
                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER, TokenKind.INDEX], tok)
                    if tok.kind   == TokenKind.REGISTER:
                        Vx  = self.parse_register(tok.value)
                        tok = next(self.tokens)
                        self.expected([TokenKind.NUMBER, TokenKind.REGISTER, TokenKind.INDEX], tok)
                        if tok.kind == TokenKind.NUMBER:
                            value = self.parse_number(tok.value)
                            opcode = (0x6000 | (Vx << 8) | ( value & 0x00ff))
                        elif tok.kind == TokenKind.INDEX:
                            opcode = (0xF065  | (Vx << 8))
                        elif tok.kind == TokenKind.REGISTER:
                            Vy = self.parse_register(tok.value)
                            opcode = (0x8000  | (Vx << 8) | (Vy << 4))
                    elif tok.kind == TokenKind.INDEX:
                        tok = next(self.tokens)
                        self.expected([TokenKind.IDENTIFIER, TokenKind.NUMBER, TokenKind.REGISTER], tok)
                        if tok.kind == TokenKind.IDENTIFIER:
                            label  = self.find_label(tok)
                            addr   = self.parse_number(label.addr)
                            opcode = (0xA000 | addr)
                        elif tok.kind == TokenKind.NUMBER:
                            addr = self.parse_number(tok.value) & 0xfff
                            opcode = (0xA000 | addr)
                        elif tok.kind == TokenKind.REGISTER:
                            Vx = self.parse_register(tok.value)
                            opcode = (0xF055 | (Vx << 8))
                    
                    self.binary.extend(to_bytes(opcode))

                elif tok.value == InstrKind.DRAW:
                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER], tok)
                    Vx = self.parse_register(tok.value)

                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER], tok)
                    Vy = self.parse_register(tok.value)

                    tok = next(self.tokens)
                    self.expected([TokenKind.NUMBER], tok)
                    nibble = self.parse_number(tok.value)

                    self.draw(Vx, Vy, nibble)

                elif tok.value == InstrKind.ADD:
                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER, TokenKind.INDEX], tok)

                    if tok.kind == TokenKind.REGISTER:
                        Vx = self.parse_register(tok.value)

                        tok = next(self.tokens)
                        self.expected([TokenKind.NUMBER, TokenKind.REGISTER], tok)

                        if tok.kind == TokenKind.NUMBER:
                            byte = self.parse_number(tok.value)
                            opcode = 0x7000 | (Vx << 8) | (0x00ff & byte)
                        elif tok.kind == TokenKind.REGISTER:
                            Vy = self.parse_register(tok.value)
                            opcode = 0x8004 | (Vx << 8) | (Vy << 4)
                    elif tok.kind == TokenKind.INDEX:
                        tok = next(self.tokens)
                        self.expected([TokenKind.REGISTER], tok)
                        Vx = self.parse_register(tok.value) & 0xf
                        opcode = (0xF01E | (Vx << 8))
                    self.binary.extend(to_bytes(opcode))
                elif tok.value == InstrKind.SUB:
                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER], tok)
                    Vx = self.parse_register(tok.value)

                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER], tok)
                    Vy = self.parse_register(tok.value)

                    # 8xy5
                    opcode = 0x8005 | (Vx << 8) | (Vy << 4)
                    self.binary.extend(to_bytes(opcode))
                elif tok.value == InstrKind.SUBN:
                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER], tok)
                    Vx = self.parse_register(tok.value)

                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER], tok)
                    Vy = self.parse_register(tok.value)

                    # 8xy7
                    opcode = 0x8007 | (Vx << 8) | (Vy << 4)
                    self.binary.extend(to_bytes(opcode))
                elif tok.value == InstrKind.SE:
                    
                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER], tok)
                    Vx = self.parse_register(tok.value)

                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER, TokenKind.NUMBER], tok)

                    if tok.kind == TokenKind.REGISTER:
                        Vy = self.parse_register(tok.value)
                        opcode = 0x5000 | (Vx << 8) |  ( Vy << 4)
                    elif tok.kind == TokenKind.NUMBER:
                        number = self.parse_number(tok.value)
                        opcode = 0x3000 | (Vx << 8) |  ( number & 0x00ff)
                    self.binary.extend(to_bytes(opcode))
                elif tok.value == InstrKind.SNE:
                    
                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER], tok)
                    Vx = self.parse_register(tok.value)

                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER, TokenKind.NUMBER], tok)

                    if tok.kind == TokenKind.REGISTER:
                        Vy = self.parse_register(tok.value)
                        opcode = 0x9000 | (Vx << 8) |  ( Vy << 4)
                    elif tok.kind == TokenKind.NUMBER:
                        number = self.parse_number(tok.value)
                        opcode = 0x4000 | (Vx << 8) |  ( number & 0x00ff)
                    self.binary.extend(to_bytes(opcode))

                elif tok.value == InstrKind.SKP:
                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER, TokenKind.NUMBER], tok)
                    key = self.parse_number(tok.value) & 0xf
                    opcode = (0xE09E | (key << 8))
                    self.binary.extend(to_bytes(opcode))
                elif tok.value == InstrKind.SKNP:
                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER, TokenKind.NUMBER], tok)
                    key = self.parse_number(tok.value) & 0xf
                    opcode = (0xE0A1 | (key << 8))
                    self.binary.extend(to_bytes(opcode))
                
                elif tok.value == InstrKind.RAND:
                    tok = next(self.tokens)
                    self.expected([TokenKind.REGISTER], tok)
                    Vx = self.parse_number(tok.value)

                    tok = next(self.tokens)
                    self.expected([TokenKind.NUMBER], tok)
                    byte = self.parse_number(tok.value)

                    self.binary.extend(to_bytes((0xC000 | (Vx  << 8) | (0x00ff & byte))))

                elif tok.value == InstrKind.CALL:
                    tok = next(self.tokens)
                    self.expected([TokenKind.IDENTIFIER, TokenKind.NUMBER], tok)

                    if tok.kind == TokenKind.IDENTIFIER:
                        label = self.find_label(tok)
                        addr  = self.parse_number(label.addr)
                    if tok.kind == TokenKind.NUMBER:
                        addr = self.parse_number(tok.value)
                    self.call(addr)
                elif tok.value == InstrKind.RET:
                    self.binary.extend(to_bytes(0x00EE))

                else: exit(f'Could not parse instruction {tok}')
            elif tok.kind == TokenKind.LABEL or tok.kind == TokenKind.EOF:
                # console.error('Unreachable')
                pass
            elif tok.kind == TokenKind.IDENTIFIER:
                console.error('Unimplemented')
            elif tok.kind == TokenKind.ALIAS:
                next(self.tokens)
                next(self.tokens)
                continue
            else: 
                print(f"\033[4;36m{self.filename}:{tok.loc.line}:{tok.loc.index}\033[0m \033[1;31m[ERROR]\033[0m Invalid token {tok}")
                exit(1)
        self.expected([TokenKind.EOF], tok)
        return self.binary
    def resolve_alias(self, tokens: list[Token]):
        tokens_iter = iter(tokens)
        for tok in tokens_iter:
            if tok.kind == TokenKind.ALIAS:

                alias_name = next(tokens_iter)
                self.expected([TokenKind.IDENTIFIER], alias_name)

                alias_body = next(tokens_iter)
                self.expected([TokenKind.REGISTER, TokenKind.NUMBER], alias_body)
                
                for index in range(len(tokens)):
                    if (tokens[index].kind == TokenKind.IDENTIFIER or tokens[index].kind == TokenKind.NUMBER) and (tokens[index].value == alias_name.value):
                        tokens[index] = Token(alias_body.kind, alias_body.value, tokens[index].loc)

                for token in tokens:
                    print(token)
    def parse_labels(self, tokens: list[Token]) -> list[Token]:
        tokens_iter = iter(tokens)
        pc = 0x200
        for tok in tokens_iter:
            if tok.kind   == TokenKind.LABEL:
                self.add_label(tok, pc)
            elif tok.kind == TokenKind.DIRECTIVE:
                if tok.value   == 'ascii':
                    tok = next(tokens_iter)
                    self.expected([TokenKind.STRING], tok)
                    pc += len(tok.value)   
                elif tok.value == 'org':
                    tok = next(tokens_iter)
                    self.expected([TokenKind.NUMBER], tok)
                    pc = self.parse_number(tok.value)               
                elif tok.value == 'font':
                    tok = next(tokens_iter)
                    self.add_label(tok, pc)
                    while True:
                        tok = next(tokens_iter)
                        if tok.value == 'endfont':
                            break
                        pc += 1
                    self.expected([TokenKind.IDENTIFIER], tok)
                elif tok.value == 'byte':
                    tok = next(tokens_iter)
                    self.expected([TokenKind.IDENTIFIER], tok)
                    identifier = tok

                    tok = next(tokens_iter)
                    self.expected([TokenKind.NUMBER], tok)
                    value = self.parse_number(tok.value)

                    self.add_label(identifier, pc)
                    pc += 2
            elif tok.kind == TokenKind.INSTRUCTION:
                pc += 2
        return self.labels
    def find_label(self, token: Token, report: bool = True):
        for label in self.labels:
            if label.token.value == token.value:
                return label
        if report is True:
            self.undefined(token)
        return None
    def add_label(self, token: Token, pc: int) -> None:
        addr = pc & 0xfff
        # check if label is already defined
        label = self.find_label(token, False)
        if label is not None: 
            self.redefinition(label)
        self.labels.append(Label(token.value, addr, token))
        # self.labels.append({
        #     'addr' : addr, 
        #     'token': token
        # })
    def parse_ascii(self, value: str) -> bytearray:
        output: bytearray = bytearray()
        for i in range(len(value)):
            output.append(ord(value[i]))
        return output
    def parse_number(self, value: str) -> int:
        if str(value)[0:2] == '0x':
            return int(value, 16)
        if value in [v for v in 'abcdef']:
            return int(value, 16)
        
        return int(value)
    def parse_register(self, value: str) -> int:
        if 0 > self.parse_number(value) < 0xf:
            exit(f"\033[1;31m[ERROR]\033[0m register must be range [0, 16]")
        return int(value, 16) & 0xf

    def call(self, addr: int) -> None:
        opcode = to_bytes(0x2000 | (addr & 0x0FFF))
        self.binary.extend(opcode)
    def jmp(self, addr: int) -> None:
        opcode = to_bytes(0x1000 | (addr & 0x0FFF))
        self.binary.extend(opcode)
    def draw(self, x: int, y: int, nibble: int) -> None:
        opcode = to_bytes(0xD000 | (x << 8) | (y << 4) | (nibble << 0))
        self.binary.extend(opcode)

    def expected(self, tokens: list[TokenKind], token: Token) -> bool:
        assert isinstance(tokens, list)
        if token.kind not in tokens:
            line  = f"{self.filename}:{token.loc.line}:{token.loc.index + 1}"
            expd  = ' '.join(t.name for t in tokens)
            error = f"Expected values of [ {expd} ], but got {token.kind}: {token.value}"
            exit(f"\033[4;36m{line}\033[0m \033[1;31m[ERROR]\033[0m {error}")
        return True
    def undefined(self, token: Token) -> None:
        line  = f"{self.filename}:{token.loc.line}:{token.loc.index + 1}"
        error = f"Name '{token.value}' is not defined"
        exit(f"\033[4;36m{line}\033[0m \033[1;31m[ERROR]\033[0m {error}")
    def redefinition(self, label: Label) -> None:
        line  = f"{self.filename}:{label.token.loc.line}:{label.token.loc.index + 1}"
        error = f"redifinition of '{label.token.value}'"
        exit(f"\033[4;36m{line}\033[0m \033[1;31m[ERROR]\033[0m {error}")

if __name__ == '__main__':
    codetest:str = """
        jmp main
        .ascii "Hello"
        main:
            add  v8  0x1
            add  v9  0x1
            load [I] 0
        inf: jmp inf
    """
    lexer  = Lexer()
    tokens = lexer.tokenize(codetest)
    for token in tokens:
        print(token)
    parser = Parser("test")
    binary = parser.parse(tokens)

    print(binary)