import re
from typing import *
from enum import Enum, auto
from dataclasses import dataclass
from collections import namedtuple
from .tokenizer  import *

class Lexer:
    keywords: list = ['jmp', 'load', 'cls', 'draw', 'add', 'rand', 'se', 'sne', 
                      'call', 'ret', 'skp', 'sknp', 'sub', 'subn']
    def __init__(self):
        self.tokens: list = []

    # https://docs.python.org/3/library/re.html#writing-a-tokenizer
    def tokenize(self, code: str) -> List[Token]:
        token_specification = [
            ('NUMBER',   r'0[xX][0-9a-fA-F]+|[0-9]+'),  # Integer or decimal number
            ('STRING',   r'\".*\"'),                    # Match string inside quotation and ""
            ('REGISTER', r'[v|V]([0-9a-fA-F]+)'),       # Match v1-vf registers
            ('REG_I',    r'\[I\]'),                     # match `i` register
            ('LABEL',    r'[A-Za-z0-9_]+\:'),           # Match Labels
            ('ID',       r'[A-Za-z0-9_]+'),             # Identifiers
            ('OP',       r'[+\-*/]'),                   # Arithmetic operators
            ('NEWLINE',  r'\n'),                        # Line endings
            ('SKIP',     r'[ \t]+'),                    # Skip over spaces and tabs
            ('DIRECTIVE',r'\.[A-Za-z0-9]+'),            # Match directive
            ('COMMA',    r'\,'),                        # Match comma
            ('COMMENT',  r';.*'),                       # Match comments
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

            if   kind == 'NUMBER':    self.tokens.append(Token(TokenKind.NUMBER,    value,      location))
            elif kind == 'STRING':    self.tokens.append(Token(TokenKind.STRING,    value[1:-1],location))
            elif kind == 'OP':        self.tokens.append(Token(TokenKind.OPERATION, value,      location))
            elif kind == 'LABEL':     self.tokens.append(Token(TokenKind.LABEL,     value[:-1], location))
            elif kind == 'DIRECTIVE': self.tokens.append(Token(TokenKind.DIRECTIVE, value[1:],  location))
            elif kind == 'REGISTER':  self.tokens.append(Token(TokenKind.REGISTER,  value[1:],  location))
            elif kind == 'REG_I':     self.tokens.append(Token(TokenKind.INDEX,     value,      location))    
            elif kind == 'NEWLINE':   line_start = mo.end(); line_num += 1
                        
            elif kind == 'ID' and value.lower() in self.keywords:
                self.tokens.append(Token(TokenKind.INSTRUCTION, self.tokenize_instr(value.upper()), location))
            elif kind == 'ID' and value not in self.keywords:
                self.tokens.append(Token(TokenKind.IDENTIFIER, value, location))
            
            elif kind in ['SKIP', 'COMMA', 'COMMENT']: continue
            elif kind == 'MISMATCH': exit(f'Unexpected token `{value!r}` at line {line_num}')

        self.tokens.append(Token(TokenKind.EOF, '\\0', location))
        return self.tokens

    def __iter__(self):
        return iter(self.tokens)

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
