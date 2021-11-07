%alias x v0
%alias y v1

main:
    load x, 0
    load y, 5
    
    if x < y begin
        load x 0
    else
        add  x 1
    end
jmp inf