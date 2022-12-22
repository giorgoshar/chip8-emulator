from typing import Optional, Any
from utils.console import console
from c8 import lexer, parser, ast, errors

# if len(sys.argv) < 3:9
#     exit('asm args error')
# filename = sys.argv[1]
# output   = sys.argv[2]
# if len(sys.argv) != 3: 
#     exit(f"Usage: {sys.argv[0]} [filename]")

def to_bytes(value: int):
    if type(value) is not int:
        console.error('Value must be an integer')
    return value.to_bytes(2, 'big')

def parse_number(value: str) -> int:
    if str(value)[0:2] == '0x':
        return int(value, 16)
    if value in [v for v in 'abcdef']:
        return int(value, 16)
    return int(value)
def parse_register(value: str) -> int:
    if 0 > parse_number(value) < 0xf:
        exit(f"\033[1;31m[ERROR]\033[0m register must be range [0, 16]")
    return int(value, 16) & 0xf

def VERIFY_LEN(args :list[Any], num :int):
    if len(args) != num:
        console.error(f"Expected len of {num} but got {len(args)}")

class Assembler:
    class OpcodeInstruction:
        def __init__(self, opcode :Optional[bytes], value :str) -> None:
            self.opcode = opcode
            self.value  = value

        def __str__(self):
            return f"<OpcodeInstruction({self.opcode}, {self.value})>"

    @staticmethod
    def make_instr_cls(node :ast.ASTNode) -> OpcodeInstruction:
        return Assembler.OpcodeInstruction(None, f"CLS")

    @staticmethod
    def make_instr_jmp(node :ast.ASTNode) -> OpcodeInstruction:
        VERIFY_LEN(node.body, 1)
        return Assembler.OpcodeInstruction(None, f"JMP __LABEL_{node.body[0]}")

    @staticmethod
    def make_instr_load(node :ast.ASTNode) -> OpcodeInstruction:
        VERIFY_LEN(node.body, 2)

        args = node.body[0].kind | node.body[1].kind
        if args == (lexer.TokenKind.REGISTER | lexer.TokenKind.NUMBER):
            Vx  = parse_register(node.body[0].value)
            num = parse_number(node.body[1].value)
            opcode = (0x6000 | (Vx << 8) | ( num & 0x00ff))
            return Assembler.OpcodeInstruction(to_bytes(opcode), f"LOAD v{node.body[0].value}, {node.body[1].value}")
        elif args == (lexer.TokenKind.REGISTER | lexer.TokenKind.REGISTER):
            Vx  = parse_register(node.body[0].value)
            Vy  = parse_register(node.body[1].value)
            opcode = (0x6000 | (Vx << 8) | ( Vy & 0x00ff))
            return Assembler.OpcodeInstruction(to_bytes(opcode), f"LOAD v{node.body[0].value}, v{node.body[1].value}")
        elif args == (lexer.TokenKind.INDEX | lexer.TokenKind.IDENTIFIER):
            return Assembler.OpcodeInstruction(None, f"LOAD [I], {node.body[1].value}")
        elif args == (lexer.TokenKind.INDEX | lexer.TokenKind.NUMBER):
            return Assembler.OpcodeInstruction(None, f"LOAD [I], {node.body[1].value}")
        else: errors.Unreachable(f"{node}") 

    @staticmethod
    def make_instr_add(node :ast.ASTNode) -> OpcodeInstruction:
        VERIFY_LEN(node.body, 2)

        args = node.body[0].kind | node.body[1].kind
        if args == (lexer.TokenKind.REGISTER | lexer.TokenKind.REGISTER):
            return Assembler.OpcodeInstruction(None, f"ADD v{node.body[0].value} v{node.body[1].value}")
        elif args == (lexer.TokenKind.REGISTER | lexer.TokenKind.NUMBER):
            return Assembler.OpcodeInstruction(None, f"ADD v{node.body[0].value} {node.body[1].value}")
        elif args == (lexer.TokenKind.INDEX | lexer.TokenKind.REGISTER):
            return Assembler.OpcodeInstruction(None, f"ADD [I] v{node.body[1].value}")
        else: errors.Unreachable(f"{node}") 
    
    @staticmethod
    def make_instr_sne(node :ast.ASTNode) -> OpcodeInstruction:
        VERIFY_LEN(node.body, 2)

        args = node.body[0].kind | node.body[1].kind
        if args == (lexer.TokenKind.REGISTER | lexer.TokenKind.NUMBER):
            return Assembler.OpcodeInstruction(None, f"SNE v{node.body[0].value} {node.body[1].value}")
        else: errors.Unreachable(f"{node}") 
    
    @staticmethod
    def make_instr_subn(node :ast.ASTNode) -> OpcodeInstruction:
        VERIFY_LEN(node.body, 2)

        args = node.body[0].kind | node.body[1].kind
        if args == (lexer.TokenKind.REGISTER | lexer.TokenKind.REGISTER):
            return Assembler.OpcodeInstruction(None, f"SUBN v{node.body[0].value} v{node.body[1].value}")
        else: errors.Unreachable(f"{node}") 

    @staticmethod
    def make_instr_call(node :ast.ASTNode) -> OpcodeInstruction:
        VERIFY_LEN(node.body, 1)
        if node.body[0].kind ==  lexer.TokenKind.IDENTIFIER:
            return Assembler.OpcodeInstruction(None, f"CALL __LABEL_{node.body[0].value}")
        else: errors.Unreachable(f"{node}") 

    @staticmethod
    def make_instr_draw(node :ast.ASTNode) -> OpcodeInstruction:
        VERIFY_LEN(node.body, 3)
        args = node.body[0].kind | node.body[1].kind | node.body[2].kind
        if args == (lexer.TokenKind.REGISTER | lexer.TokenKind.REGISTER | lexer.TokenKind.NUMBER):
            return Assembler.OpcodeInstruction(None, f"DRAW v{node.body[0].value} v{node.body[1].value} {node.body[2].value}")
        else: errors.Unreachable(f"{node}") 
    
    @staticmethod
    def make_instr_ret(node :ast.ASTNode) -> OpcodeInstruction:
        return Assembler.OpcodeInstruction(to_bytes(0x00EE), f"RET")
    
    @staticmethod
    def make_dir_mem(node :ast.ASTNode) -> OpcodeInstruction:
        VERIFY_LEN(node.body, 2) # identifier, bytes
        return Assembler.OpcodeInstruction(node.body[0], f"MEM")

    @staticmethod
    def make_dir_font(node :ast.ASTNode) -> OpcodeInstruction:
        print(node)
        VERIFY_LEN(node.body, 2)
        font_bytes = f" ".join([hex(x) for x in node.body[1]])
        return Assembler.OpcodeInstruction(None, f".font {node.body[0].value} {font_bytes}, endfont")

class Generator:
    def __init__(self, program: ast.ProgramNode):
        self.program :ast.ProgramNode = program
        self.asm     :list[Assembler.OpcodeInstruction] = []

    def compile(self):
        console.info("Compiling")
        self.visitor(self.program)
        console.info("Compiling ended")

        asm: str = ""
        for op in self.asm:
            asm += op.value + "\n"
        with open("test-c8-asm.asm", 'w') as fp:
            fp.write(asm)
        print(asm)

    def visitor(self, node: ast.ASTNode) -> None:
        console.info(f"Visiting node {node}")
        match node.kind:
            case ast.NodeKind.SCOPE: self.visit_scope(node)
            case ast.NodeKind.INSTR: self.visit_instr(node)
            case _: errors.Unreachable(f"Unreachable NodeKind: {node.kind}")

    def visit_scope(self, node: ast.ASTNode) -> None:
        self.asm.append(Assembler.OpcodeInstruction(None, f"__LABEL_{node.name}:"))
        for child in node.children:
            self.visitor(child)

    def visit_instr(self, node: ast.ASTNode) -> None:
        console.info(f"Visiting instr {node}")

        asm: Optional[Assembler.OpcodeInstruction] = None
        match node.instr:
            case lexer.InstrKind.CLS:  asm = Assembler.make_instr_cls(node)
            case lexer.InstrKind.JMP:  asm = Assembler.make_instr_jmp(node)
            case lexer.InstrKind.LOAD: asm = Assembler.make_instr_load(node)
            case lexer.InstrKind.ADD:  asm = Assembler.make_instr_add(node)
            case lexer.InstrKind.SNE:  asm = Assembler.make_instr_sne(node)
            case lexer.InstrKind.CALL: asm = Assembler.make_instr_call(node)
            case lexer.InstrKind.DRAW: asm = Assembler.make_instr_draw(node)
            case lexer.InstrKind.RET:  asm = Assembler.make_instr_ret(node)
            case lexer.InstrKind.SUBN: asm = Assembler.make_instr_subn(node)
            case lexer.DirectiveKind.MEM:  asm = Assembler.make_dir_mem(node)
            case lexer.DirectiveKind.FONT: asm = Assembler.make_dir_font(node)
            case lexer.DirectiveKind.ASCII: return
            case _: errors.Unreachable(str(node))
        
        if asm.__class__.__name__ != 'OpcodeInstruction':
            errors.Unreachable(str(node))
        self.asm.append(asm)


filename = "./test.c8"
output   = "test"

source = lexer.Source(filename)
lex    = lexer.Lexer(source)
tokens = lex.tokenize(source.code)

c8_parser = parser.Parser(source, lex)
c8_ast    = c8_parser.parse_program()

compiler = Generator(c8_ast)
compiler.compile()

for asm in compiler.asm:
    print(asm)

# with open(output, 'wb') as fp:
#     fp.write(binary)
# fullpath = os.getcwd() + output
# console.info(f"bin : {fullpath}")
# console.info(f"size: {len(binary)}bytes")