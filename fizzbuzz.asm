.org 0x200
jmp main
.byte i 0
.byte cur_x 0
.byte cur_y 0

main:
    load v5 10
    loop:
        load [I] i
        load v1, [I]
        add  v1, 1
        load [I], v1

        ; move cursor
        cls
        se v1 v5
        call DRAW_NUMBER
        call FIZZ
        call BUZZ

    jmp loop
    
    jmp inf
inf: jmp inf

load_pos:
    ; load x position
    load [I] cur_x
    load v8, [I]
    ; add  v8, 1
    load [I], v8

    ; load y position
    load [I] cur_y
    load v9, [I]
    add  v9, 1
    load [I], v9

    ret

check_pos:

FIZZ:

    load v9 0 ; y position
    load v8 0 ; x position
    call load_pos

    load v8, 0
    load [I], letter_F
    draw v8, v9, 5

    add v8, 4
    load [I], letter_I
    draw v8, v9, 5

    add v8, 2
    load [I], letter_Z
    draw v8, v9, 5

    add v8, 4
    load [I], letter_Z
    draw v8, v9, 5

    ret
BUZZ:

    load v9 0 ; y position
    load v8 0 ; x position

    load [I], letter_B
    draw v8, v9, 5

    add v8, 4
    load [I], letter_U
    draw v8, v9, 5
    
    add v8, 4
    load [I], letter_Z
    draw v8, v9, 5

    add v8, 4
    load [I], letter_Z
    draw v8, v9, 5

    ret
DRAW_NUMBER:
    load v8, 0 ; x position
    load v9, 0 ; y position

    load [I], 0
    draw v8, v9, 5
    ret

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
.font letter_F 0xE0 0x80 0xC0 0x80 0x80, endfont
.font letter_I 0x80 0x80 0x80 0x80 0x80, endfont
.font letter_Z 0xE0 0x20 0x40 0x80 0xE0, endfont
.font letter_B 0xC0 0xA0 0xE0 0xA0 0xC0, endfont
.font letter_U 0xA0 0xA0 0xA0 0xA0 0xE0, endfont


.font letter_QMARK    0xF0 0x10 0x70 0x00 0x40, endfont
.font letter_EXCLMARK 0xF0 0x10 0x70 0x00 0x40, endfont

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
