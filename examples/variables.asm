.org 0x200
jmp main

.var x 1
.var y 1
.var speed 1
main:
    ; load v2, 1
    ; load v1, 1

    loop: jmp again
    again:
        
        load [I] x
        load v1, [I]
        add v1, 1
        load [I] v1
        load v1, v5

        jmp loop
    jmp inf
inf: jmp inf

err:
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

.font letter_A 0x1c 0x22 0x3e 0x22 0x22, endfont
.font letter_E 0x7c 0x40 0x7c 0x40 0x7c, endfont
.font letter_R 0x7c 0x44 0x7c 0x78 0x44, endfont
.font letter_D 0x78 0x44 0x44 0x44 0x78, endfont
.font letter_O 0x7c 0x44 0x44 0x44 0x7c, endfont
.font letter_N 0x44 0x64 0x54 0x4c 0x44, endfont
.font square   0xfc 0xfc 0xfc 0xfc 0xfc, endfont
.font person   0x70 0x70 0x20 0x70 0xA8 0x20 0x50 0x50, endfont