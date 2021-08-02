.org 0x200
jmp main
.ascii  "test loops"
main:
    count:
        load [I], 0x0         ; set i = 0, start of 0 number int fonts
        load v3,  0           ; index number font in memory
        next:
            cls               ; clear screen
            load v1,  1       ; x position
            load v2,  1       ; y position
            add  [I], v3      ; i += v3
            draw v1,  v2, 5   ; draw from v1 to v2, 5 bytes of font
            add  v3,  5       ; v3 + 5
            se   v3,  15      ; if v3 == 5 skip next instruction
            jmp next          ; jump to next
            jmp count
loop:
    jmp loop