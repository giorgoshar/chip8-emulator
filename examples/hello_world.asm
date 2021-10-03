.org 0x200
jmp main
main:
    load v9, 0xf

    load v1, 0
    load [I], letter_H
    draw v1, v2, 5

    add v1 6
    load [I], letter_E
    draw v1, v2, 5

    add v1 5
    load [I], letter_L
    draw v1, v2, 5

    add v1 5
    load [I], letter_L
    draw v1, v2, 5

    add v1 5
    load [I], letter_O
    draw v1, v2, 5

    add v2 6
    load v1, 0
    load [I], letter_W
    draw v1, v2, 5

    add v1 6
    load [I], letter_O
    draw v1, v2, 5
    
    add v1 5
    load [I], letter_R
    draw v1, v2, 5

    add v1 5
    load [I], letter_L
    draw v1, v2, 5
    
    add v1 5
    load [I], letter_D
    draw v1, v2, 5

    jmp inf
inf: jmp inf

.font letter_E 0xE0 0x80 0xC0 0x80 0xE0, endfont
.font letter_D 0xC0 0xA0 0xA0 0xA0 0xC0, endfont
.font letter_O 0xE0 0xA0 0xA0 0xA0 0xE0, endfont
.font letter_H 0x88 0x88 0xF8 0x88 0x88, endfont
.font letter_L 0x80 0x80 0x80 0x80 0xE0, endfont
.font letter_W 0x88 0x88 0xA8 0xA8 0xF8, endfont
.font letter_R 0xE0 0xA0 0xE0 0xC0 0xA0, endfont