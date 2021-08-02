.org 0x200
jmp main
.ascii  "Simple MAZE implementation"
main:
    load v0, 0        ; x position
    load v1, 0        ; y position
loop:
    load [I], LEFT    
    rand v2, 1
    se   v2, 1
    load [I], RIGHT
    draw v0, v1, 4
    
    add  v0, 4
    se   v0, 64
    jmp  loop
    load v0, 0
    add  v1, 4
    se   v1, 32
    jmp  loop
end:
    jmp end
.font RIGHT
    "*       "
    " *      "
    "  *     "
    "   *    "
    "        "
.font LEFT
    "   *    "
    "  *     "
    " *      "
    "*       "
    "        "
