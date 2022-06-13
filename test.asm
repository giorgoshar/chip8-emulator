jmp main
.ascii "Hello"

main:
    load v5 0
    load v6 45
    loop:
        
        ; load vf v6
        ; subn vf v5
        ; sne  vf 0
        ; 
        ; jmp end_if
        ;     call reset
        ; end_if:
        ; 
        ; load v5 v1
        ; call drawnumber
        ; call increment

        if v6 < v5 begin 
            call reset
            add v8 0x1
            add v9 0x1
        end
        load v5 v1
        call drawnumber
        call increment

    jmp loop
jmp inf

reset:
    load [I] counter
    load v0 0x0
    load v1 0x0
    load [I] v1
    ret

; increament by v3
increment:
    load v3 0x5      ; step increment
    load [I] counter ; load addr counter to I
    load v1 [I]      ; store bytes of I to in to v0..v1
    add v1 v3        ; v1 = v1 + v3
    load [I] counter ; load addr counter to I
    load [I] v1      ; store bytes of to v0..v1 to in I..
    ret

drawnumber:
    cls
    load va, 0   ; pos_x
    load vb, 0   ; pos_y
    load [I] 0
    add  [I] v5
    draw va vb 5
    ret
inf: jmp inf   

.mem counter 0x0000
.mem posX    0x00
.mem posY    0x00