
from typing      import *
from asm.lexer   import *
from asm.tparser import *

class Compiler:
    def __init__(self, ast: Scope):
        self.ast: Scope = ast
        self.ptr: int   = 0x200

    def compile_instruction(self, instr: Instruction):
        pass

    def compile(self):
        console.info('Start Compiling...')
        self.ptr = 0x200

        for node in self.ast.body:
            print(node)

        console.info('Compiler end')