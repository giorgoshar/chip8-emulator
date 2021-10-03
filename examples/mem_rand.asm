.org 0x200
.inc "letters.inc"
jmp main
main:

loop:
    load [I], 0x230
    rand v1, 1
    rand v2, 2
    rand v3, 3
    rand v4, 4
    rand v5, 5

    load [I], v5
    jmp  loop
    ; jmp done
inf: 
    jmp inf
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
    load [I], letter_A
    draw v1, v2, 5

    jmp inf

.font letter_E 0x7c 0x40 0x7c 0x40 0x7c
.font letter_R 0x7c 0x44 0x7c 0x78 0x44
.font letter_D 0x78 0x44 0x44 0x44 0x78
.font letter_O 0x7c 0x44 0x44 0x44 0x7c
.font letter_N 0x44 0x64 0x54 0x4c 0x44
.font letter_A 0x1c 0x22 0x3e 0x22 0x22