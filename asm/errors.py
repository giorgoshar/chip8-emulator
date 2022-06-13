import re
import sys
from typing import *
from enum import Enum, auto
from dataclasses import dataclass
from collections import namedtuple
from utils.console import console
from asm.tokenizer import *

class UndefinedError:
    def __init__(self, filename: str, token: Token):
        line  = f"{filename}:{token.loc.line}:{token.loc.index + 1}"
        error = f"Undefined name `{token.value}`"
        console.error(f"\033[4;36m{line}\033[0m {error}")

class UnExpectedError:
    def __init__(self, filename: str, tokens: list, token: Token) -> bool:
        if token.kind not in tokens:
            line  = f"{filename}:{token.loc.line}:{token.loc.index + 1}"
            expd  = ' '.join(t.name for t in tokens)
            error = f"expected values of [ {expd} ], but got {token.kind}: {token.value}"
            console.error(f"\033[4;36m{line}\033[0m {error}")

class RedifinitionError:
    def __init__(self, filename: str, label: Dict[str, Token]):
        line  = f"{filename}:{label['token'].loc.line}:{label['token'].loc.index + 1}"
        error = f"redifinition of '{label['token'].value}'"
        console.error(f"\033[4;36m{line}\033[0m {error}")