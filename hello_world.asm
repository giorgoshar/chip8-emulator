.org 0x200
jmp main
main:
    

    load v1, 1
    load v2, 1
    load [I], letter_H
    draw v1, v2, 5

    load v1, 5
    load v2, 1
    load [I], letter_E
    draw v1, v2, 5

    load v1, 9
    load v2, 1
    load [I], letter_L
    draw v1, v2, 5

    load v1, 13
    load v2, 1
    load [I], letter_L
    draw v1, v2, 5
    
    load v1, 17
    load v2, 1
    load [I], letter_O
    draw v1, v2, 5

    load v1, 23
    load v2, 1
    load [I], letter_W
    draw v1, v2, 5

    load v1, 29
    load v2, 1
    load [I], letter_O
    draw v1, v2, 5
    
    load v1, 33
    load v2, 1
    load [I], letter_R
    draw v1, v2, 5

    load v1, 37
    load v2, 1
    load [I], letter_L
    draw v1, v2, 5
    
    load v1, 41
    load v2, 1
    load [I], letter_D
    draw v1, v2, 5

    jmp inf
inf: jmp inf

.font letter_A 0xF8 0xA8 0xA8 0xA8 0xA8, endfont
.font letter_E 0xE0 0x80 0xC0 0x80 0xE0, endfont
.font letter_D 0xC0 0xA0 0xA0 0xA0 0xC0, endfont
.font letter_O 0xE0 0xA0 0xA0 0xA0 0xE0, endfont
.font letter_N 0x44 0x64 0x54 0x4c 0x44, endfont
.font letter_H 0xA0 0xA0 0xE0 0xA0 0xA0, endfont
.font letter_L 0x80 0x80 0x80 0x80 0xE0, endfont
.font letter_G 0x70 0x80 0xB0 0x90 0x70, endfont
.font letter_P 0xF0 0x90 0x90 0xF0 0x80, endfont
.font letter_W 0x88 0x88 0xA8 0xA8 0xF8, endfont
.font letter_R 0xE0 0xA0 0xE0 0xC0 0xA0, endfont

.font letter_QMARK    0xF0 0x10 0x70 0x00 0x40, endfont
.font letter_EXCLMARK 0xF0 0x10 0x70 0x00 0x40, endfont

.font letter_TEST 0x80 0x60 0x10 0xE0 0x90, endfont


err:
    cls
    load v1, 1
    load v2, 1
    load [I], letter_E
    draw v1, v2, 5

    load v1, 7
    load v2, 1
    load [I], letter_R
    draw v1, v2, 5

    load v1, 13
    load v2, 1
    load [I], letter_R
    draw v1, v2, 5
    
    jmp inf
done:
    cls
    load v1, 1
    load v2, 1
    load [I], letter_D
    draw v1, v2, 5

    load v1, 7
    load v2, 1
    load [I], letter_O
    draw v1, v2, 5

    load v1, 13
    load v2, 1
    load [I], letter_N
    draw v1, v2, 5

    load v1, 19
    load v2, 1
    load [I], letter_E
    draw v1, v2, 5

    jmp inf
