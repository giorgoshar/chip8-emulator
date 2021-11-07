%alias x v0
%alias y v1

main:
    load x, 0
    load y, 5

    loop:
    ; if x < y
        load v2 y
        subn v2 x
        sne  vf 0x0

        jmp if_x_less_y_body 
        jmp if_x_less_y_else ; else jmp

        if_x_less_y_body:
            call DrawNumber
            add  x 0x1
            jmp loop
    ; else
        if_x_less_y_else:
            call DrawNumber
            load x  0x
            load v2 0x0
    jmp loop
jmp inf

DrawNumber:
    cls
    load va, 0
    load vb, 0
    load [I] 0
    add  [I] v0
    draw va vb 5
    ret

inf: jmp inf