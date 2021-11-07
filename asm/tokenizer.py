from typing import *
from enum import Enum, auto
from dataclasses import dataclass
from collections import namedtuple

Loc = namedtuple('Loc', ['line', 'index'])

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
    OPERATION   = auto()
    IDENTIFIER  = auto()
    ALIAS       = auto()
    STATEMENT   = auto()
    BINOP       = auto()
    EOF         = auto()

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

@dataclass
class Token: 
    kind : TokenKind
    value: Any
    loc  : Loc

    def __str__(self):
        return f'{self.kind:30} {self.value:<20} Location:{self.loc}'
