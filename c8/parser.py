from c8.lexer  import *
from c8.errors import *
from c8.ast    import *
from utils.console import console

def to_bytes(value: int):
    if type(value) is not int:
        console.error('Value must be an integer')
    return value.to_bytes(2, 'big')

class Parser:
    def __init__(self, source: Source, lex: Lexer):
        self.source  :Source    = source
        self.lexer   :Lexer     = lex
    
    # start parsing from here
    def parse_program(self, lex: Optional[Lexer] = None) -> ProgramNode:
        if lex is None: lex = self.lexer
        lex.reset_index()
        Program = ProgramNode('Program')
        self.parse(lex, Program)
        Program.print()
        return Program

    # parse instructions
    def parse_instr_load(self, lex: Lexer) -> Instruction:
        arg1 = lex.next()
        self.expected([TokenKind.REGISTER, TokenKind.INDEX], arg1)

        arg2 = lex.next()
        match arg1.kind:
            case TokenKind.REGISTER: self.expected([TokenKind.REGISTER, TokenKind.NUMBER, TokenKind.INDEX],      arg2)
            case TokenKind.INDEX:    self.expected([TokenKind.REGISTER, TokenKind.NUMBER, TokenKind.IDENTIFIER], arg2)
            case _: raise Unreachable(str(token))
        return Instruction(InstrKind.LOAD, [arg1, arg2])

    def parse_instr_call(self, lex: Lexer) -> Instruction:
        arg1 = lex.next()
        self.expected([TokenKind.IDENTIFIER], arg1)
        return Instruction(InstrKind.CALL, [arg1])

    def parse_instr_jmp(self, lex: Lexer) -> Instruction:
        self.expected([TokenKind.IDENTIFIER], lex.next())
        name: Token = lex.peek()
        return Instruction(InstrKind.JMP, [name.value])

    def parse_instr_add(self, lex: Lexer) -> Instruction:

        arg1 = lex.next()
        self.expected([TokenKind.REGISTER, TokenKind.INDEX], arg1)
        
        arg2 = lex.next()
        self.expected([TokenKind.REGISTER, TokenKind.NUMBER], arg2)

        return Instruction(InstrKind.ADD, [arg1, arg2])

    def parse_instr_sne(self, lex: Lexer) -> Instruction:
        arg1 = lex.next()
        self.expected([TokenKind.REGISTER], arg1)
        
        arg2 = lex.next()
        self.expected([TokenKind.REGISTER, TokenKind.NUMBER], arg2)

        return Instruction(InstrKind.SNE, [arg1, arg2])
    
    def parse_instr_subn(self, lex: Lexer) -> Instruction:
        
        arg1 = lex.next()
        self.expected([TokenKind.REGISTER], arg1)
        
        arg2 = lex.next()
        self.expected([TokenKind.REGISTER, TokenKind.NUMBER], arg2)

        return Instruction(InstrKind.SUBN, [arg1, arg2])

    def parse_instr_draw(self, lex: Lexer) -> Instruction:
        arg1 = lex.next()
        self.expected([TokenKind.REGISTER], arg1)

        arg2 = lex.next()
        self.expected([TokenKind.REGISTER], arg2)

        arg3 = lex.next()
        self.expected([TokenKind.NUMBER], arg3)

        return Instruction(InstrKind.DRAW, [arg1, arg2, arg3])

    # parse directives
    def parse_dir_ascii(self, lex: Lexer) -> Directive:
        token = lex.next()
        return Directive(DirectiveKind.ASCII, [token.value])

    def parse_dir_mem(self, lex: Lexer) -> Directive:
        identifier = lex.next()
        self.expected([TokenKind.IDENTIFIER], identifier)
        mem = bytearray()
        while True:
            token = lex.next()
            if token.kind != TokenKind.NUMBER: 
                break
            self.expected([TokenKind.NUMBER], token)
            mem.append(self.parse_number(token.value))
        
        return Directive(DirectiveKind.MEM, [identifier, mem])

    def parse_dir_font(self, lex: Lexer) -> Directive:
        identifier = lex.next()
        self.expected([TokenKind.IDENTIFIER], identifier)
        font_bytes = bytearray()
        while True:
            token = lex.next()
            if token.value == 'endfont': 
                break
            self.expected([TokenKind.NUMBER], token)
            font_bytes.append(self.parse_number(token.value))
        
        token = lex.peek()
        self.expected([TokenKind.IDENTIFIER], token)
        
        if token.value != 'endfont': 
            console.error(f"parse_directive: {token}")
        return Directive(DirectiveKind.FONT, [identifier, font_bytes])

    # main parsing
    def parse_directive(self, lex: Lexer) -> Directive:
        token = lex.peek()
        match token.value:
            case 'ascii': return self.parse_dir_ascii(lex)
            case 'font':  return self.parse_dir_font(lex)
            case 'mem':   return self.parse_dir_mem(lex)
            case _: raise Unreachable(str(token))

    def parse_instr(self, lex: Lexer) -> Instruction:
        token = lex.peek()
        match token.value:
            case InstrKind.JMP:  return self.parse_instr_jmp(lex)
            case InstrKind.CALL: return self.parse_instr_call(lex)
            case InstrKind.LOAD: return self.parse_instr_load(lex)
            case InstrKind.ADD:  return self.parse_instr_add(lex)
            case InstrKind.SNE:  return self.parse_instr_sne(lex)
            case InstrKind.DRAW: return self.parse_instr_draw(lex)
            case InstrKind.SUBN: return self.parse_instr_subn(lex)
            case InstrKind.CLS:  return Instruction(InstrKind.CLS, [])
            case InstrKind.RET:  return Instruction(InstrKind.RET, [])
            case _: raise Unreachable(str(token))
    
    def parse_function(self, lex: Lexer, current_scope: ScopeNode) -> FunctionDefinition:
        
        # check if is FN_REF
        if lex.peek().kind != TokenKind.FN_REF:
            raise Unreachable('parse_function')
        
        identifier = lex.next()

        # check if identifier already in current scope
        for child in current_scope.children:
            if child is None: continue
            if child.__class__.__name__ == 'FunctionDefinition' and child.name == identifier.value:
                err_line = f"\033[4;36m{lex.source.filename}:{identifier.loc.line}:{identifier.loc.index}\033[0m"
                err_msg  = f"\033[4;36m{lex.source.filename}:{child.token.loc.line}:{child.token.loc.index}\033[0m"
                console.error(f"{err_line} function `{identifier.value}` already defined at {err_msg}")
        
        self.expected([TokenKind.IDENTIFIER], identifier)
        self.expected([TokenKind.OBRACKET],   lex.next())
        lex.next()

        fn_node: FunctionDefinition = FunctionDefinition(identifier.value, identifier)
        self.parse(lex, fn_node)
        self.expected([TokenKind.CBRACKET], lex.peek())
        return fn_node

    def parse_if(self, lex: Lexer, node: ASTNode):

        operand1 = lex.next()
        self.expected([TokenKind.REGISTER], operand1)

        operator = lex.next()
        self.expected([TokenKind.OPERATOR], operator)

        operand2 = lex.next()
        self.expected([TokenKind.NUMBER], operand2)

        expr1 = Expression(None, operand1, None)
        expr2 = Expression(None, operand2, None)

        expr = Expression(expr1, operator, expr2)
        console.info(f"Expr -> {expr}")

        end_expr = lex.next()
        self.expected([TokenKind.OBRACKET], end_expr)
        lex.next()

        body_block :ScopeNode = ScopeNode('if_stmt_01')
        while lex.peek().kind != TokenKind.CBRACKET:
            if lex.peek().kind == TokenKind.EOF:
                self.expected([TokenKind.CBRACKET], lex.peek())
            self.parse(lex, body_block)
        if_node: IfStatement = IfStatement(expr, body_block)

        return if_node

    def parse(self, lex: Lexer, node: ScopeNode) -> ASTNode:
        while lex.has_more():
            token: Token = lex.peek()

            # we really expcted the end of some statement...
            self.expected([
                    TokenKind.INSTRUCTION, 
                    TokenKind.DIRECTIVE, 
                    TokenKind.FN_REF, 
                    TokenKind.CBRACKET, 
                    TokenKind.IF
                ], 
                token
            )

            match token.kind:
                case TokenKind.INSTRUCTION:
                    node.add_children(self.parse_instr(lex))
                case TokenKind.DIRECTIVE:
                    node.add_children(self.parse_directive(lex))
                case TokenKind.FN_REF:
                    fn = self.parse_function(lex, node)
                    node.add_children(fn)
                case TokenKind.IF:
                    eef = self.parse_if(lex, node)
                    node.add_children(eef)
                case TokenKind.CBRACKET:
                    break
                case _: raise Unreachable(str(token))
            lex.next()
        return node

    # parse primitive types
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

    # error functions
    def expected(self, tokens: list[TokenKind], token: Token) -> bool:
        assert isinstance(tokens, list)
        if token.kind not in tokens:
            line  = f"{self.source.filename}:{token.loc.line}:{token.loc.index + 1}"
            expd  = ' '.join(str(t.name) for t in tokens)
            error = f"Expected values of [ {expd} ], but got {token.kind}: {token.value}"
            exit(f"\033[4;36m{line}\033[0m \033[1;31m[ERROR]\033[0m {error}")
        return True
    def undefined(self, token: Token) -> None:
        line  = f"{self.source.filename}:{token.loc.line}:{token.loc.index + 1}"
        error = f"Name '{token.value}' is not defined"
        exit(f"\033[4;36m{line}\033[0m \033[1;31m[ERROR]\033[0m {error}")
    def redefinition(self, label: dict[str, Token]) -> None:
        line  = f"{self.source.filename}:{label['token'].loc.line}:{label['token'].loc.index + 1}"
        error = f"redifinition of '{label['token'].value}'"
        exit(f"\033[4;36m{line}\033[0m \033[1;31m[ERROR]\033[0m {error}")

if __name__ == '__main__':

    source = Source()
    source.set_code("""
        jmp main
        .ascii "Hello"
        main:
            add  v8  0x1
            add  v9  0x1
            load [I] 0
        inf: jmp inf
    """)

    lexer  = Lexer(source)
    tokens = lexer.tokenize(source.code)
    for token in tokens:
        print(token)
    parser = Parser(source, lexer)
    binary = parser.parse_program(lexer)
    print(binary)