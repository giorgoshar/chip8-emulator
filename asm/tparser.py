import enum
from typing import *
from utils.console import console
from asm.lexer import *

INDENT_LEVEL = 4
def TEXT_RED(text:str):   return f"\033[1;31m{text}\033[0m"
def TEXT_GREEN(text:str): return f"\033[1;32m{text}\033[0m"


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

class Scope:
    def __init__(self, name:str):
        self.name:str       = name
        self.body:list[Any] = []
        self.vars:list[Any] = []

    def add(self, node: Any):
        self.body.append(node)
    
    def print(self, ident:int = 0):
        ident += INDENT_LEVEL
        print("".rjust(ident, ' '), str(self))

        for vars in self.vars:
            vars.print(ident)

        for statement in self.body:
            statement.print(ident)
        
    def __str__(self):
        return f"Scope(name: {self.name})"

class Font:
    def __init__(self, name: str, binary: bytearray):
        self.name = name
        self.value      = binary
    
    def __str__(self):
        return f"Font(name{ self.name }, binary: { self.binary })"

    def print(self, ident=0):
        ident += INDENT_LEVEL
        print("".rjust(ident, ' '), str(self))

class Directive:
    def __init__(self, type:str, value:Any):
        self.type  = type
        self.value = value
    
    def print(self, ident=0):
        ident += INDENT_LEVEL
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
        ident += INDENT_LEVEL
        print("".rjust(ident, ' '), str(self))

class FuncDeclaration(Scope):
    def __init__(self, name: str):
        Scope.__init__(self, name)
    
    def __str__(self):
        return f"FuncDeclaration(name: {self.name})"
    
    def print(self, ident=0):
        ident += INDENT_LEVEL
        print("".rjust(ident, ' '), str(self))
        
        for vars in self.vars:
            vars.print(ident)

        for statement in self.body:
            statement.print(ident)
    
class VarDeclaration:
    def __init__(self, name: str, value: Any):
        self.name:str  = name
        self.value:Any = value
    
    def __str__(self):
        return f"VarDeclaration(name: {self.name}, value: {self.value})"

    def print(self, ident=0):
        ident += INDENT_LEVEL
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
                self.lexer.next()
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

        kind:InstrKind = self.lexer.peek().value
        args:list      = []

        match self.lexer.peek().value:
            case InstrKind.JMP:
                self.lexer.eat([TokenKind.IDENTIFIER, TokenKind.NUMBER])
                if self.lexer.peek() == TokenKind.IDENTIFIER:
                    args.append(self.lexer.peek())
                if self.lexer.peek() == TokenKind.NUMBER:
                    addr = self.parse_number(self.lexer.peek().value)

            case InstrKind.LOAD:
                self.lexer.next()
                if self.lexer.peek() == TokenKind.REGISTER:
                    Vx  = self.parse_register(self.lexer.peek().value)
                    args.append(('Vx', Vx))
                    self.lexer.next()

                    if self.lexer.peek() == TokenKind.NUMBER:
                        value = self.parse_number(self.lexer.peek().value)
                        opcode = (0x6000 | (Vx << 8) | ( value & 0x00ff))
                        args.append(('number', value))

                    elif self.lexer.peek() == TokenKind.INDEX:
                        opcode = (0xF065  | (Vx << 8))
                    elif self.lexer.peek() == TokenKind.REGISTER:
                        Vy = self.parse_register(self.lexer.peek().value)
                        opcode = (0x8000  | (Vx << 8) | (Vy << 4))
                    else: 
                        self.expected([TokenKind.NUMBER, TokenKind.INDEX, TokenKind.REGISTER])
                
                elif self.lexer.peek() == TokenKind.INDEX:
                    self.lexer.eat([TokenKind.IDENTIFIER, TokenKind.NUMBER, TokenKind.REGISTER])
                    if self.lexer.peek() == TokenKind.IDENTIFIER:
                        label  = self.find_label(self.lexer.peek())
                        addr   = self.parse_number(label.addr)
                        opcode = (0xA000 | addr)
                    elif self.lexer.peek() == TokenKind.NUMBER:
                        addr = self.parse_number(self.lexer.peek().value) & 0xfff
                        opcode = (0xA000 | addr)
                    elif self.lexer.peek() == TokenKind.REGISTER:
                        Vx = self.parse_register(self.lexer.peek().value)
                        opcode = ( (0xF055 | (Vx << 8)) ) & 0xffff
            case _:
                console.error(f"Could not parse instruction: {self.lexer.peek() }")
        
        self.lexer.next()
        return Instruction(kind, args)

    def parse_function(self) -> Scope:
        # Get function identifier/name
        self.expected([TokenKind.FUNC])
        func_decl = FuncDeclaration(self.lexer.peek().value)
        
        self.expected([TokenKind.IDENTIFIER])
        self.expected([TokenKind.OBRACKET])

        # maybe return the body and append like:
        # func_body = self.parse_block(func_decl)
        self.parse_block(func_decl)
        
        self.expected([TokenKind.CBRACKET])
        
        return func_decl
    
    def parse_anonymous_block(self) -> Scope:

        self.expected([TokenKind.OBRACKET])

        block = Scope('AnonBlock')
        self.parse_block(block)

        self.expected([TokenKind.CBRACKET])
        return block

    def parse_variable(self):
        
        identifier = self.lexer.peek()
        
        self.expected([TokenKind.IDENTIFIER])
        self.expected([TokenKind.ASSIGN])

        value:Any  = self.lexer.peek()
        identifier = VarDeclaration(identifier, value)

        self.lexer.next()
        self.expected([TokenKind.END])

        return identifier

    def parse_block(self, scope: Scope) -> Scope:
        while self.lexer.peek() != TokenKind.EOF:
            # print(f'[{TEXT_RED(scope.name):^20}] Parsing:', self.lexer.peek())
            match self.lexer.peek():
                case TokenKind.DIRECTIVE:
                    directive = self.parse_directive()
                    scope.body.append(directive)
                
                case TokenKind.INSTRUCTION:
                    instruction = self.parse_instruction()
                    scope.body.append(instruction)
        
                case TokenKind.IDENTIFIER:
                    identifier = self.parse_variable()
                    scope.vars.append(identifier)

                case TokenKind.FUNC:
                    function = self.parse_function()
                    scope.body.append(function)

                case TokenKind.OBRACKET:
                    block = self.parse_anonymous_block()
                    scope.body.append(block)
                
                case TokenKind.CBRACKET:
                    break
                    # console.error('CBRACKET on exit')
                case _:
                    console.error(f"Could not parse block: { self.lexer.peek() }")
        return scope

    def parse(self) -> Scope:
        self.lexer.reset()

        console.info("Parsing lexer to AST")
        ast: Scope = self.parse_block(self.program)
        ast.print(0)
        console.info("Parsing end")
        return ast

    def parse_labels(self):
        pointer: int = 0x200
        offset : int = 0
        self.lexer.reset()
        
        while self.lexer.peek() != TokenKind.EOF:
            match self.lexer.peek():
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

    def expected(self, expected:list[TokenKind]):
        if self.lexer.peek().kind not in expected:
            token = self.lexer.peek()
            line  = f"{self.filename}:{token.loc.line}:{token.loc.index + 1}"
            expd  = ' or '.join(t.name for t in expected)
            error = f"Expected {expd} but got kind:{token.kind}, value:{token.value}"
            console.error(f"\033[4;36m{line}\033[0m {error}")
        self.lexer.next()
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

