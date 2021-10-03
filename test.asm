.org 0x200
jmp main
.ascii "Hello World"
.byte x 0
.byte y 0
.byte n 0
main:
    load vf, 0
    load v5, 0
    loop:
        cls
        call load8
        load v1, v6
        call draw_number
        jmp loop
    jmp inf
inf: jmp inf

load8:
    load [I], x
    load [I], v1
    load [I], 0
    ret

draw_number:
    call print
    ret
print:
   draw v4, v5, 5
   ret 

.font letter_A 0x1c 0x22 0x3e 0x22 0x22, endfont
.font letter_E 0x7c 0x40 0x7c 0x40 0x7c, endfont
.font letter_R 0x7c 0x44 0x7c 0x78 0x44, endfont
.font letter_D 0x78 0x44 0x44 0x44 0x78, endfont
.font letter_O 0x7c 0x44 0x44 0x44 0x7c, endfont
.font letter_N 0x44 0x64 0x54 0x4c 0x44, endfont

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
