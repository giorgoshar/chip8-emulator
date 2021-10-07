.org 0x200
jmp main
.byte n 0x0000
main:
    load v4, 0
    load v5, 0
    load v0, 0
    loop:
        call inc_n
        sne v0 0x2d
        call reset
        jmp loop
    jmp inf
inf: jmp inf

reset:
    cls
    load [I] n   ; load addr n in [I]
    load v0 0    ; set v0 to 0
    load [I] v0  ; store V0...Vx in memory addr stored in [I]
    ret

inc_n:
    cls
    load [I] n            ; load addr n in [I]
    load v0 [I]           ; store values of addr [I] in regs V0...Vx
    add  v0 5             ; add v0 5
    load [I] n            ; load again mem addr n to [I]
    load [I] v0           ; store V0...Vx to addr in memory starting at [I]
    load [I] 0            ; set [I] to 0
    add  [I] v0           ; [I] += v0
    draw v4, v5, 5        ; draw
    ret

font_start:
.font letter_A 0x20 0x50 0x88 0xF8 0x88, endfont
.font letter_E 0xF8 0xC0 0xF0 0xC0 0xF8, endfont
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
