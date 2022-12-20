import os
import sys
sys.path.append('C:\\Users\\User\\Desktop\\Giorgos\\Dev\\emulators\\chip8')

import re
from typing import Any
from enum import Enum, auto
from dataclasses import dataclass
from utils.console import console

@dataclass
class Loc:
    line  :int = 0
    index :int = 0
    def __str__(self) -> str:
        return f"@Loc({self.line}:{self.index})"

class TokenKind(Enum):
    NEWLINE     = auto()
    NUMBER      = auto()
    STRING      = auto()
    REGISTER    = auto()
    INDEX       = auto()
    LABEL       = auto()
    DIRECTIVE   = auto()
    INSTRUCTION = auto()
    SKIP        = auto()
    COMMA       = auto()
    COMMENT     = auto()
    ERROR       = auto()
    OPERATOR    = auto()
    IDENTIFIER  = auto()
    ALIAS       = auto()
    STATEMENT   = auto()
    ASSIGN      = auto()
    BINOP       = auto()
    EOF         = auto()
    INVALID     = auto()
class StmtKind(Enum):
    IF    = auto()
    ELIF  = auto()
    ELSE  = auto()
    WHILE = auto()
    BEGIN = auto()
    END   = auto()
    ERROR = auto()
class InstrKind(Enum):
    CLS   = auto()
    JMP   = auto()
    CALL  = auto()
    RET   = auto()
    LOAD  = auto()
    ADD   = auto()
    SUB   = auto()
    SUBN  = auto()
    RAND  = auto()
    DRAW  = auto()
    SE    = auto()
    SNE   = auto()
    SKP   = auto()
    SKNP  = auto()
    ERROR = auto()
class BinOpKind(Enum):
    EQ      = auto()
    NEQ     = auto()
    GREATER = auto()
    LESS    = auto()
    LEQ     = auto()
    GEQ     = auto()
    ERROR   = auto()
class TokenType(Enum):
    u8  = auto()
    u16 = auto()

@dataclass
class Token: 
    kind : TokenKind
    value: Any
    loc  : Loc
    def __str__(self):
        return f'{self.kind:30} {self.value:<20} Location:{self.loc}'

@dataclass
class Label:
    name : str
    addr : int
    token: Token

class Source:
    def __init__(self, filename: str = ""):
        self.filename :str = filename
        self.code     :str = ""
        if self.filename != "":
            self.read()
    
    def read(self, filename: str = ""):
        if filename: 
            self.filename = filename
        if not os.path.exists(self.filename):
            console.error(f"file '{self.filename}' does not exist")
        with open(self.filename, 'r') as fp:
            self.code = fp.read()
        return self.code

class Lexer:
    keywords: list[str] = [
        'jmp', 'call', 'ret', 'cls', 'load', 'draw', 'skp', 'sknp', 
        'add', 'rand', 'se', 'sne', 'sub', 'subn',
    ]
    
    def __init__(self, source: Source):
        self.source :Source       = source
        self.tokens :list[Token]  = []
        self.index  :int          = 0

    def next(self) -> Token:
        if not self.has_more():
            return self.set_invalid_token()
        self.index = self.index + 1
        return self.tokens[self.index]
    
    def peek(self) -> Token:
        return self.tokens[self.index]

    def eat(self, kind:list[TokenKind]) -> Token:
        if not self.has_more():
            return self.set_invalid_token()

        if self.tokens[self.index + 1].kind not in kind:
            return self.set_invalid_token()

        self.next()
        return self.peek()
    
    def has_more(self) -> bool:
        return (self.index + 1) < len(self.tokens)
    
    def lookahead(self) -> Token:
        if not self.has_more(): 
            return self.set_invalid_token()
        return self.tokens[self.index + 1]

    def reset(self): 
        self.index = 0

    def set_invalid_token(self) -> Token:
        return Token(TokenKind.INVALID, "", Loc(-1, -1))

    def __iter__(self):
        return iter(self.tokens)
    
    def tokenize(self, code: str) -> list[Token]:
        token_specification = [
            ('NUMBER',   r'0[xX][0-9a-fA-F]+|[0-9]+'),  # Integer or decimal number
            ('STRING',   r'\".*\"'),                    # Match string inside quotation and ""
            ('REGISTER', r'[v|V]([0-9a-fA-F]+)'),       # Match v1-vf registers
            ('REG_I',    r'\[I\]'),                     # match `i` register
            ('LABEL',    r'[A-Za-z0-9_]+\:'),           # Match Labels
            ('ID',       r'[A-Za-z0-9_]+'),             # Identifiers
            ('OP',       r'[>=]{2}|[<=]{2}|[+\-*<>]'),  # Arithmetic/Unary operators
            ('NEWLINE',  r'\n'),                        # Line endings
            ('SKIP',     r'[ \t]+'),                    # Skip over spaces and tabs
            ('DIRECTIVE',r'\.[A-Za-z0-9]+'),            # Match directive
            ('COMMA',    r'\,'),                        # Match comma
            ('COMMENT',  r';.*'),                       # Match comments
            ('ALIAS',    r'%alias'),                    # Match alias
            ('ASSIGN',   r':='),                        # Match := assignment operator
            ('OBRACKET', r'{'),                         # Match { Open  bracket
            ('CBRACKET', r'}'),                         # Match } close bracket
            ('MISMATCH', r'.'),                         # Any other character
        ]
        tok_regex  = '|'.join(r'(?P<%s>%s)' % pair for pair in token_specification)
        line_num   = 1
        line_start = 0
        for mo in re.finditer(tok_regex, code):
            kind     = mo.lastgroup
            value    = mo.group()
            column   = mo.start() - line_start
            location = Loc(line_num, column)
            match kind:
                case 'NUMBER':    self.tokens.append(Token(TokenKind.NUMBER,    value,      location))
                case 'STRING':    self.tokens.append(Token(TokenKind.STRING,    value[1:-1],location))
                case 'OP':        self.tokens.append(Token(TokenKind.OPERATOR,  self.tokenize_binop(value),      location))
                case 'LABEL':     self.tokens.append(Token(TokenKind.LABEL,     value[:-1], location))
                case 'DIRECTIVE': self.tokens.append(Token(TokenKind.DIRECTIVE, value[1:],  location))
                case 'REGISTER':  self.tokens.append(Token(TokenKind.REGISTER,  value[1:],  location))
                case 'REG_I':     self.tokens.append(Token(TokenKind.INDEX,     value,      location))    
                case 'ID':
                    if value.lower() in self.keywords:
                        self.tokens.append(Token(TokenKind.INSTRUCTION, self.tokenize_instr(value.upper()), location))
                    else:
                        self.tokens.append(Token(TokenKind.IDENTIFIER, value, location))
                case 'ASSIGN':    self.tokens.append(Token(TokenKind.ASSIGN,    value, location))
                case 'ALIAS':     self.tokens.append(Token(TokenKind.ALIAS,     value, location))
                case 'STATEMENT': self.tokens.append(Token(TokenKind.STATEMENT, value, location))
                case 'NEWLINE':   line_start = mo.end(); line_num += 1
                case 'SKIP', 'COMMA', 'COMMENT': continue
                case 'MISMATCH': 
                    print(f"\033[4;36m{self.source.filename}:{line_num}:{column}\033[0m \033[1;31m[ERROR]\033[0m Invalid token")
                    exit(1)

        self.tokens.append(Token(TokenKind.EOF, '\\0', Loc(line_num, line_start)))
        self.token = self.tokens[self.index]
        return self.tokens

    def tokenize_instr(self, keyword: str) -> InstrKind:
        if keyword == 'JMP' : return InstrKind.JMP
        if keyword == 'LOAD': return InstrKind.LOAD
        if keyword == 'CLS' : return InstrKind.CLS
        if keyword == 'DRAW': return InstrKind.DRAW
        if keyword == 'ADD' : return InstrKind.ADD
        if keyword == 'RAND': return InstrKind.RAND
        if keyword == 'SE'  : return InstrKind.SE
        if keyword == 'SNE' : return InstrKind.SNE
        if keyword == 'CALL': return InstrKind.CALL
        if keyword == 'RET' : return InstrKind.RET
        if keyword == 'SKP' : return InstrKind.SKP
        if keyword == 'SKNP': return InstrKind.SKNP
        if keyword == 'SUB' : return InstrKind.SUB
        if keyword == 'SUBN': return InstrKind.SUBN
        return InstrKind.ERROR

    def tokenize_stmnt(self, keyword: str) -> StmtKind:
        if keyword == 'IF'   : return StmtKind.IF
        if keyword == 'ELSE' : return StmtKind.ELSE
        if keyword == 'END'  : return StmtKind.END
        if keyword == 'BEGIN': return StmtKind.BEGIN

        return StmtKind.ERROR
    
    def tokenize_binop(self, keyword: str) -> BinOpKind:
        if keyword == '==': return BinOpKind.EQ
        if keyword == '!=': return BinOpKind.NEQ
        if keyword == '>' : return BinOpKind.GREATER
        if keyword == '<' : return BinOpKind.LESS
        
        return BinOpKind.ERROR

if __name__ == '__main__':
    code:str = "jmp main"
    lex    = Lexer()
    tokens = lex.tokenize(code)
    for token in tokens:
        print(token)