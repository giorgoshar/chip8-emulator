.org 0x200
jmp main
.ascii  "test loops"
main:
    count:
        load [I], 0x0         ; set i = 0, start of 0 number int fonts
        next:
            cls               ; clear screen
            load v1,  1        ; x position
            load v2,  1        ; y position
            load v3,  5        ; index number font in memory
            add  [I], v3      ; i += v3
            draw v1,  v2, 5    ; draw from v1 to v2 5 bytes of font
            rand v4,  0x1
            se   v4,  1        ; if v3 == 5 skip next instection
            jmp next          ; jump to next
loop:
    jmp loop