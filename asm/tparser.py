import enum
from typing import *
from utils.console import console
from asm.lexer     import *

TREE_IDENT = 4

def TEXT_RED(text:str):
    return f"\033[1;31m{text}\033[0m"

class StatementKind(enum.Enum):
    FuncDeclaration = 0

class Scope: pass
class Statement: pass
class FuncDeclaration: pass
class VarDeclaration: pass

class Assembler:
    @staticmethod
    def jmp(addr:int):
        return 0x1000 | (addr & 0x0FFF)
    def call(addr:int):
        return 0x2000 | (addr & 0x0FFF)
    def ret():
        return 0x00EE
    def rand_Vx_kk(Vx:int, byte:int):
        return 0xC000 | (Vx  << 8) | (0x00ff & byte)

class Font:
    def __init__(self, name: str, binary: bytearray):
        self.name = name
        self.value      = binary
    
    def __str__(self):
        return f"Font(name{ self.name }, binary: { self.binary })"

    def print(self, ident=0):
        ident += TREE_IDENT
        print("".rjust(ident, ' '), str(self))

class Directive:
    def __init__(self, type:str, value:Any):
        self.type  = type
        self.value = value
    
    def print(self, ident=0):
        ident += TREE_IDENT
        spacing = "".rjust(ident, ' ')
        if self.type == 'font':
            print(spacing, f"Font: ", end='')
            self.value.print(ident)
        else:
            print(spacing, str(self))
    
    def __str__(self):
        return f"Directive(type: {self.type}, value: {self.value})"

class Instruction:
    def __init__(self, kind: InstrKind, args: List[Any]):
        self.kind = kind
        self.args = args
    
    def eval(self) -> bytearray:
        output = bytearray()
        match self.kind:
            case InstrKind.JMP:
                addr   = self.args[0]
                output = Assembler.jmp(addr)
        return output
    
    def __str__(self):
        return f"Instruction(kind: {self.kind} args: {self.args})"

    def print(self, ident: int = 0):
        ident += TREE_IDENT
        print("".rjust(ident, ' '), str(self))


class Scope:
    def __init__(self, name:str):
        self.name:str       = name
        self.body:list[Any] = []

    def add(self, node: Any):
        self.body.append(node)
    
    def print(self, ident:int = 0):
        ident += TREE_IDENT
        print("".rjust(ident, ' '), str(self))
        for statement in self.body:
            statement.print(ident)
    
    def __str__(self):
        return f"Scope(name: {self.name})"

class FuncDeclaration(Scope):
    def __init__(self, name: str):
        Scope.__init__(self, name)
    
    def __str__(self):
        return f"FuncDeclaration(name: {self.name})"
    
    def print(self, ident=0):
        ident += TREE_IDENT
        print("".rjust(ident, ' '), str(self))
        for statement in self.body:
            statement.print(ident)
    
class VarDeclaration:
    def __init__(self, name: str, value: Any):
        self.name:str  = name
        self.value:Any = value
    
    def __str__(self):
        return f"VarDeclaration(name: {self.name}, value: {self.value})"

    def print(self, ident=0):
        ident += TREE_IDENT
        print("".rjust(ident, ' '), str(self))

class Parser:
    def __init__(self, lex: Lexer, filename: str = "test"):
        self.filename: str             = filename
        self.lexer   : Lexer           = lex
        self.labels  : List[Label]     = []
        self.program : Scope           = Scope("Program")

    def parse_directive(self) -> bytearray:
        output = bytearray()
        
        match self.lexer.peek().value:
            case 'ascii':
                self.lexer.eat([TokenKind.STRING])
                value = self.parse_ascii(self.lexer.peek().value)
                return Directive('ascii', value)
            case 'org':
                self.lexer.next()
                output = bytearray()
            case 'font':
                self.lexer.eat([TokenKind.IDENTIFIER])
                identifier = self.lexer.peek().value
                font_bytes = bytearray()
                while self.lexer.lookahead().value != 'endfont':
                    if (self.lexer.peek() == TokenKind.EOF) or (self.lexer.peek() == TokenKind.INVALID):
                        exit("EOF | INVALID on font")
                    self.lexer.eat([TokenKind.NUMBER])
                    font_bytes.append(self.parse_number(self.lexer.peek().value))
                self.lexer.eat([TokenKind.IDENTIFIER])
                output = bytearray(font_bytes)
            case 'mem':
                self.lexer.eat([TokenKind.IDENTIFIER])
                identifier = self.lexer.peek()
                self.lexer.eat([TokenKind.NUMBER])
                number = self.parse_number(self.lexer.peek().value)
                opcode = 0xFFFF & number
                output = bytearray(opcode)
            case _:
                console.error(f"Could not parse directive: { self.token }")
        return output

    def parse_instruction(self):
        output = bytearray()

        kind:InstrKind = self.lexer.peek().value
        args:list      = []
        
        match self.lexer.peek().value:
            
            case InstrKind.JMP:
                self.lexer.eat([TokenKind.IDENTIFIER, TokenKind.NUMBER])
                if self.lexer.peek().kind == TokenKind.IDENTIFIER:
                    return Instruction(InstrKind.JMP, [ self.lexer.peek() ])
                if self.lexer.peek().kind == TokenKind.NUMBER:
                    addr = self.parse_number(self.lexer.peek().value)
                opcode = Assembler.jmp(addr)
                output = self.to_binary(opcode)
            case InstrKind.CALL:
                self.lexer.next()
                self.expected(self.lexer, [TokenKind.IDENTIFIER, TokenKind.NUMBER])
                if self.lexer.peek().kind == TokenKind.IDENTIFIER:
                    label = self.find_label(self.lexer.peek())
                    addr  = self.parse_number(label.addr)
                if self.lexer.peek().kind == TokenKind.NUMBER:
                    addr = self.parse_number(self.lexer.peek().value)
                opcode = Assembler.call(addr)
                output = self.to_binary(opcode)
            case InstrKind.RET:
                opcode = Assembler.ret()
                output = self.to_binary(opcode)
            case InstrKind.RAND:
                self.lexer.eat([TokenKind.REGISTER])
                Vx = self.parse_number(self.lexer.peek().value)

                self.lexer.eat([TokenKind.NUMBER])
                byte = self.parse_number(self.lexer.peek().value)

                opcode = Assembler.rand_Vx_kk(Vx, byte)
                output = self.to_binary(opcode)
            case InstrKind.ADD:
                self.lexer.eat([TokenKind.REGISTER, TokenKind.INDEX])
                if   self.lexer.peek().kind == TokenKind.REGISTER:
                    Vx = self.parse_register(self.lexer.peek().value)
                    self.lexer.eat([TokenKind.NUMBER, TokenKind.REGISTER])
                    if self.lexer.peek().kind == TokenKind.NUMBER:
                        byte = self.parse_number(self.lexer.peek().value)
                        opcode = 0x7000 | (Vx << 8) | (0x00ff & byte)
                    elif self.lexer.peek().kind == TokenKind.REGISTER:
                        Vy = self.parse_register(self.lexer.peek().value)
                        opcode = 0x8004 | (Vx << 8) | (Vy << 4)
                elif self.lexer.peek().kind == TokenKind.INDEX:
                    self.lexer.eat([TokenKind.REGISTER])
                    Vx = self.parse_register(self.lexer.peek().value) & 0xf
                    opcode = (0xF01E | (Vx << 8))
                output = self.to_binary(opcode)
            case InstrKind.LOAD:
                self.lexer.eat([TokenKind.REGISTER, TokenKind.INDEX])
                args = []

                if self.lexer.peek().kind == TokenKind.REGISTER:
                    Vx  = self.parse_register(self.lexer.peek().value)
                    self.lexer.eat([TokenKind.NUMBER, TokenKind.REGISTER, TokenKind.INDEX])
                    args.append(('Vx', Vx))
                    if self.lexer.peek().kind == TokenKind.NUMBER:
                        value = self.parse_number(self.lexer.peek().value)
                        opcode = (0x6000 | (Vx << 8) | ( value & 0x00ff))
                        args.append(('number', value))
                    elif self.lexer.peek().kind == TokenKind.INDEX:
                        opcode = (0xF065  | (Vx << 8))
                    elif self.lexer.peek().kind == TokenKind.REGISTER:
                        Vy = self.parse_register(self.lexer.peek().value)
                        opcode = (0x8000  | (Vx << 8) | (Vy << 4))
                elif self.lexer.peek().kind == TokenKind.INDEX:
                    self.lexer.eat([TokenKind.IDENTIFIER, TokenKind.NUMBER, TokenKind.REGISTER])
                    if self.lexer.peek().kind == TokenKind.IDENTIFIER:
                        label  = self.find_label(self.lexer.peek())
                        addr   = self.parse_number(label.addr)
                        opcode = (0xA000 | addr)
                    elif self.lexer.peek().kind == TokenKind.NUMBER:
                        addr = self.parse_number(self.lexer.peek().value) & 0xfff
                        opcode = (0xA000 | addr)
                    elif self.lexer.peek().kind == TokenKind.REGISTER:
                        Vx = self.parse_register(self.lexer.peek().value)
                        opcode = ( (0xF055 | (Vx << 8)) ) & 0xffff
                output = self.to_binary(opcode)
            case InstrKind.SUB:
                self.lexer.eat([TokenKind.REGISTER])
                Vx = self.parse_register(self.lexer.peek().value)

                self.lexer.eat([TokenKind.REGISTER])
                Vy = self.parse_register(self.lexer.peek().value)
                # 8xy5
                opcode = 0x8005 | (Vx << 8) | (Vy << 4)
                output = self.to_binary(opcode)
            case InstrKind.SUBN:
                self.lexer.eat([TokenKind.REGISTER])
                Vx = self.parse_register(self.lexer.peek().value)

                self.lexer.eat([TokenKind.REGISTER])
                Vy = self.parse_register(self.lexer.peek().value)

                # 8xy7
                opcode = 0x8007 | (Vx << 8) | (Vy << 4)
                output = self.to_binary(opcode)
            case InstrKind.SNE:
                self.lexer.eat([TokenKind.REGISTER])
                Vx = self.parse_register(self.lexer.peek().value)

                self.lexer.eat([TokenKind.REGISTER, TokenKind.NUMBER])
                if self.lexer.peek().kind == TokenKind.REGISTER:
                    Vy = self.parse_register(self.lexer.peek().value)
                    opcode = 0x9000 | (Vx << 8) |  ( Vy << 4)
                elif self.lexer.peek().kind == TokenKind.NUMBER:
                    number = self.parse_number(self.lexer.peek().value)
                    opcode = 0x4000 | (Vx << 8) |  ( number & 0x00ff)
                output = self.to_binary(opcode)
            case InstrKind.SE:
                self.lexer.eat([TokenKind.REGISTER])
                Vx = self.parse_register(self.lexer.peek().value)

                self.lexer.eat([TokenKind.REGISTER, TokenKind.NUMBER])
                if self.lexer.peek().kind == TokenKind.REGISTER:
                    Vy = self.parse_register(self.lexer.peek().value)
                    opcode = 0x5000 | (Vx << 8) |  ( Vy << 4)
                elif self.lexer.peek().kind == TokenKind.NUMBER:
                    number = self.parse_number(self.lexer.peek().value)
                    opcode = 0x3000 | (Vx << 8) |  ( number & 0x00ff)
                    output = self.to_binary(opcode)
            case InstrKind.SKP:
                self.lexer.eat([TokenKind.REGISTER, TokenKind.NUMBER])
                key = self.parse_number(self.lexer.peek().value) & 0xf
                opcode = (0xE09E | (key << 8))
                output = self.to_binary(opcode)
            case InstrKind.SKNP:
                self.lexer.eat([TokenKind.REGISTER, TokenKind.NUMBER])
                key = self.parse_number(self.lexer.peek().value) & 0xf
                opcode = (0xE0A1 | (key << 8))
                output = self.to_binary(opcode)
            case InstrKind.DRAW:
                self.lexer.eat([TokenKind.REGISTER])
                Vx = self.parse_register(self.lexer.peek().value)

                self.lexer.eat([TokenKind.REGISTER])
                Vy = self.parse_register(self.lexer.peek().value)

                self.lexer.eat([TokenKind.NUMBER])
                nibble = self.parse_number(self.lexer.peek().value)

                opcode = (0xD000 | (Vx << 8) | (Vy << 4) | (nibble << 0)).to_bytes(2, 'big')
                output = opcode
            case InstrKind.CLS:
                output = 0x00E0.to_bytes(2, 'big')
            case _:
                console.error(f"Could not parse instruction: { self.token }")
        
        return Instruction(kind, args)
        return output

    def parse_function(self) -> Scope:
        
        # Get function identifier/name
        self.lexer.eat([TokenKind.IDENTIFIER])
        func_decl = FuncDeclaration(self.lexer.peek().value)
        self.lexer.next()
        
        # must eat {
        self.lexer.eat([TokenKind.OBRACKET])
        self.lexer.next()
        
        self.parse_block(func_decl)
        
        # most eat }
        self.lexer.eat([TokenKind.CBRACKET])
        # self.lexer.next()
        
        return func_decl
    
    def parse_anonymous_block(self, scope: Scope) -> Scope:
        return self.parse_block(scope)

    def parse_identifier(self):
        console.warn(f"parse_identifier { self.lexer.peek() }")
        
        identifier = self.lexer.peek() #
        self.lexer.next()

        self.lexer.eat([TokenKind.ASSIGN])
        self.lexer.next()

        value:Any = self.lexer.peek()
        self.lexer.next()
        
        self.lexer.eat([TokenKind.END])

        identifier = VarDeclaration(identifier, value)
        # print(self.lexer.peek())
        # exit()
        return identifier
    
    def parse_block(self, scope: Scope) -> Scope:
        while self.lexer.peek() != TokenKind.EOF:
            print(f'[{TEXT_RED(scope.name):^20}] Parsing:', self.lexer.peek())
            match self.lexer.peek():
                case TokenKind.DIRECTIVE:
                    directive = self.parse_directive()
                    scope.body.append(directive)
                case TokenKind.INSTRUCTION:
                    instruction = self.parse_instruction()
                    scope.body.append(instruction)
        
                case TokenKind.IDENTIFIER:
                    identifier = self.parse_identifier()
                    scope.body.append(identifier)
                
                case TokenKind.FUNC:
                    function = self.parse_function()
                    scope.body.append(function)

                case TokenKind.OBRACKET:
                    self.lexer.next()
                    block = self.parse_anonymous_block(scope)
                    scope.body.append(block)
                case TokenKind.CBRACKET:
                    break
                case _:
                    console.error(f"[parse_block]Could not parse { self.lexer.peek() }")
            self.lexer.next()
        
        return scope

    def parse(self) -> bytearray:
        self.parse_labels()
        self.lexer.reset()
        output:bytearray = bytearray()
        
        self.parse_block(self.program)
        self.program.print(0)

        print(self.program.body[3].body)

        exit('EXIT PROGRAM')
        return output

    def parse_labels(self):
        pointer: int = 0x200
        offset : int = 0
        self.lexer.reset()
        
        while self.lexer.peek().kind != TokenKind.EOF:
            match self.lexer.peek().kind:
                case TokenKind.LABEL:
                    self.labels.append(Label(self.lexer.peek().value, pointer, token))
                case TokenKind.DIRECTIVE:
                    if self.lexer.peek().value == 'ascii':
                        offset += 1
                        token = self.lexer.next()
                        self.expected(self.lexer, [TokenKind.STRING])
                        pointer += len(self.lexer.peek().value)   
                    elif self.lexer.peek().value == 'org':
                        offset += 1
                        token = self.lexer.next()
                        self.expected(self.lexer, [TokenKind.NUMBER])
                        pointer = self.parse_number(self.lexer.peek().value)               
                    elif self.lexer.peek().value == 'font':
                        offset += 1
                        token = self.lexer.next()
                        self.labels.append(Label(self.lexer.peek().value, pointer, token))
                        while True:
                            offset += 1
                            token = self.lexer.next()
                            if self.lexer.peek().value == 'endfont':
                                break
                            pointer += 1
                        self.expected(self.lexer, [TokenKind.IDENTIFIER])
                    elif self.lexer.peek().value == 'mem':
                        offset += 1
                        token = self.lexer.next()
                        self.expected(self.lexer, [TokenKind.IDENTIFIER])
                        identifier_name = self.lexer.peek().value

                        offset += 1
                        token = self.lexer.next()
                        self.expected(self.lexer, [TokenKind.NUMBER])

                        self.labels.append(Label(identifier_name, pointer, token))
                        pointer += 2
                case TokenKind.INSTRUCTION: 
                    pointer += 2
                case TokenKind.STATEMENT:
                    if self.lexer.peek().value == StmtKind.IF: pointer += 8
            offset += 1
            self.lexer.next()
        return self.labels
    
    def find_label(self, token: Token):
        for label in self.labels:
            if label.name == token.value:
                return label
        self.undefined(token)
    def print_labels(self):
        for label in self.labels:
            print(label)

    def expected(self, lexer:Lexer, expected_kinds:list[TokenKind]) -> bool:
        assert isinstance(lexer, Lexer)
        if lexer.peek().kind not in expected_kinds:
            token = lexer.peek()
            line  = f"{self.filename}:{token.loc.line}:{token.loc.index + 1}"
            expd  = ' or '.join(t.name for t in expected_kinds)
            error = f"Expected {expd} but got kind:{token.kind}, value:{token.value}"
            console.error(f"\033[4;36m{line}\033[0m {error}")
    def undefined(self, token: Token) -> None:
        line  = f"{self.filename}:{token.loc.line}:{token.loc.index + 1}"
        error = f"Undefined name `{token.value}`"
        console.error(f"\033[4;36m{line}\033[0m {error}")
    def redefinition(self, label: Dict[str, Token]) -> None:
        line  = f"{self.filename}:{label['token'].loc.line}:{label['token'].loc.index + 1}"
        error = f"redifinition of '{label['token'].value}'"
        console.error(f"\033[4;36m{line}\033[0m {error}")

    @staticmethod
    def to_binary(opcode: int) -> bytes:
        return opcode.to_bytes(2, 'big')
    @staticmethod
    def parse_ascii(value: str) -> bytearray:
        output: bytearray = bytearray()
        for i in range(len(value)):
            output.append(ord(value[i]))
        return output
    @staticmethod
    def parse_number(value: str) -> int:
        if str(value)[0:2] == '0x':
            return int(value, 16)
        if value in [v for v in 'abcdef']:
            return int(value, 16)
        return int(value)
    @staticmethod
    def parse_register(value: str) -> int:
        if 0 > Parser.parse_number(value) < 0xf:
            exit(f"\033[1;31m[ERROR]\033[0m register must be range [0, 16]")
        return int(value, 16) & 0xf

if __name__ == '__main__':
    code:str = """
        jmp main
        .ascii "Hello"
        main:
            add  v8  0x1
            add  v9  0x1
            load [I] 0
        inf: jmp inf
    """
    lex = Lexer(code)
    # while(lexer.peek().kind != TokenKind.EOF):
    #     if lexer.token.kind == TokenKind.INVALID:
    #         break
    #     lexer.next()
    
    parser = Parser(lex, "aa")
    parser.parse()
    parser.print_labels()