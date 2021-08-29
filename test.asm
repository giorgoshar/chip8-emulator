.org 0x200
jmp main
.var x 1
.var y 1
.var speed 1
main:
    load v4, 1
    load v5, 1

    again:
        sknp 0x0 ;W
        call PERSON_MOVE_UP

        sknp 0x1 ;S
        call PERSON_MOVE_DOWN

        sknp 0xd ;D
        call PERSON_MOVE_RIGHT

        sknp 0xa ;A
        call PERSON_MOVE_LEFT
        
        sknp 0xf ;F
        call SPAWN_BOX

        cls
        call DRAW_BOXES
        call DRAW_PERSON
        jmp again

    jmp inf
inf: jmp inf

DRAW_PERSON:
    load [I], person
    draw v4, v5, 8
    ret

SPAWN_BOX:
    ret

DRAW_BOXES:
    ret

PERSON_MOVE_DOWN:
    load [I] y
    load v1, [I]
    add  v1, 1
    load [I], v1
    load v5, v1
    ret

PERSON_MOVE_UP:
    load [I] y
    load v1, [I]
    load v7, 1
    sub  v1, v7
    load [I], v1
    load v5, v1
    ret

PERSON_MOVE_RIGHT:
    load [I] x
    load v1, [I]
    add  v1, 1
    load [I], v1
    load v4, v1
    ret

PERSON_MOVE_LEFT:
    load [I] x
    load v1, [I]
    load v7, 1
    sub  v1, v7
    load [I], v1
    load v4, v1
    ret

.font letter_A 0x1c 0x22 0x3e 0x22 0x22, endfont
.font letter_E 0x7c 0x40 0x7c 0x40 0x7c, endfont
.font letter_R 0x7c 0x44 0x7c 0x78 0x44, endfont
.font letter_D 0x78 0x44 0x44 0x44 0x78, endfont
.font letter_O 0x7c 0x44 0x44 0x44 0x7c, endfont
.font letter_N 0x44 0x64 0x54 0x4c 0x44, endfont
.font square   0xfc 0xfc 0xfc 0xfc 0xfc, endfont
.font person   0x70 0x70 0x20 0x70 0xA8 0x20 0x50 0x50, endfont

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
