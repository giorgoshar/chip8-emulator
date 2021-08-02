.org   0x200
jmp    main
.ascii  "directive ascii text test"
main:
SMILE:
    load    v1,  1        ; x position
    load    v2,  1        ; y position
    load    v3,  5        ; set register v3 number
    load    [I], 0x0      ; draw number
    add     [I], 0x3      ; i += Vx
    draw    v1,  v2, 5    ; draw at screen pixels starting from i + 5
loop:
    jmp     loop