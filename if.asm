main:
    load v5, 0
    load v6, 50
    loop:
        if v5 < v6 begin
            load v5 0
            load v7 7
            load v8 8
        end
        call DrawNumber
        add v5 5
    jmp loop
jmp inf

DrawNumber:
    cls
    load va, 0
    load vb, 0
    load [I] 0
    add  [I] v5
    draw va vb 5
    ret
inf: jmp inf