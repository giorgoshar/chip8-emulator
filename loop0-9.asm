jmp main
.ascii "Hello"

main:
    load v5 0
    load v6 50
    loop:
        load vf v6
        subn vf v5
        sne  vf 0
        jmp end_if
            load v5 0
            load v7 7
            load v8 8
        end_if:
        call drawnumber
        add v5 5
    jmp loop
jmp inf

drawnumber:
    cls
    load va, 0
    load vb, 0
    load [I] 0
    add  [I] v5
    draw va vb 5
    ret
inf: jmp inf