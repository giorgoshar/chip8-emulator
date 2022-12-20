
jmp main
.ascii "Hello"

main:
    load v1 1
    load v2 2
    add  v1 v2
    sne  v1, 3
    call drawSmile
inf: jmp inf

drawSmile:
    load    v1, 5
    load    v2, 5
    load    [I], l_SMILE
    draw    v1, v2, 5
    ret
.font l_SMILE 0x18 0x48 0x08 0x48 0x18, endfont