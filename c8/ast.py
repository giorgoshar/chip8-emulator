from typing    import Optional
from enum      import auto, Enum
from c8.lexer  import *
from c8.errors import *

TREE_IDENT_STEP = 4

class NodeKind(Enum):
    INSTR         = auto()
    DIRECTIVE     = auto()
    SCOPE         = auto()
    FUNC_DEF      = auto()
    PROGRAM       = auto()
    EXPR          = auto()
    BLOCK         = auto()
    STMNT         = auto()
    IF_STMNT      = auto()
    ERROR         = auto()
    INVALID       = auto()

class ASTNode:
    def __init__(self, kind: NodeKind):
        self.kind     :NodeKind        = kind
        self.body     :list[Any]       = []
        self.instr    :Optional[Any]   = None
        self.name     :str             = ""
        self.children :list[Any]       = []

        self.value     :Optional[Any]     = None
        self.leftleaf  :Optional[ASTNode] = None
        self.rightleaf :Optional[ASTNode] = None

    def add_children(self, children: 'ASTNode'):
        self.children.append(children)
    def set_left(self, node:'ASTNode') -> None:
        self.left = node
    def set_right(self, node:'ASTNode') -> None:
        self.right = node
    def print(self, indent :int = 0) -> None:
        raise NotImplementedError

class Instruction(ASTNode):
    def __init__(self, instr :InstrKind, body: list[Token]):
        ASTNode.__init__(self, NodeKind.INSTR)
        self.instr  = instr
        self.body   = body

    def print(self, indent: int = 0):
        print(' ' * indent, self)
    
    def __str__(self):
        return f"<Instruction({self.instr}, {self.body})>"

class Directive(ASTNode):
    def __init__(self, drct :DirectiveKind, body: list[Any]):
        ASTNode.__init__(self, NodeKind.INSTR)
        self.instr = drct
        self.body  = body
    
    def print(self, indent: int = 0):
        print(' ' * indent, self)
    
    def __str__(self):
        return f"<Directive({self.body})>"

class ScopeNode(ASTNode):
    def __init__(self, name: str, token: Optional[Token] = None):
        ASTNode.__init__(self, NodeKind.SCOPE)
        self.name  = name
        self.token = token

    def print(self, indent: int = 0) -> None:
        print(' ' * indent, self)
        for children in self.children:
            children.print(indent + TREE_IDENT_STEP)

    def __str__(self):
        return f"<ScopeNode({self.name}, {len(self.children)})>"

class Expression(ASTNode):
    def __init__(self, left: Optional[ASTNode], value: Any, right: Optional[ASTNode]):
        ASTNode.__init__(self, NodeKind.EXPR)
        self.leftleaf  = left
        self.value     = value
        self.rightleaf = right

class ProgramNode(ScopeNode): pass

class FunctionDefinition(ScopeNode):
    def __str__(self):
        return f"<FunctionDefinition({self.name})>"

class IfStatement(ASTNode):
    def __init__(self, expr: Expression, block :ScopeNode):
        ASTNode.__init__(self, NodeKind.IF_STMNT)
        self.expr  :Expression = expr
        self.block :ScopeNode  = block

if __name__ == '__main__':
    pass