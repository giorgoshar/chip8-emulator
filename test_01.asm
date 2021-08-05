.org 0x200
jmp main

main:

    load v1, 0 ; load register v1 0x0
    se   v1, 0 ; if v1 == 0 skip next instruction
    jmp  err   ; else jmp err
    
    sne  v1, 1 ; if v1 != 1 skip next instruction
    jmp  err   ; else jmp err

    add v1, 1  ; add 1 to v1 register
    sne v1, 2  ; if v1 != 2 skip next instruction
    jmp err    ; else jmp err

    load v1, 0
    call addition
    se   v1, 5
    jmp err

    jmp  done

inf: 
    jmp inf

addition:
    load v2, 5
    add  v1, v2
    ret

err:
    load v1, 1
    load v2, 1
    load [I], ascii_E
    draw v1, v2, 5

    load v1, 7
    load v2, 1
    load [I], ascii_R
    draw v1, v2, 5

    load v1, 13
    load v2, 1
    load [I], ascii_R
    draw v1, v2, 5

    jmp inf
done:
    load v1, 1
    load v2, 1
    load [I], ascii_D
    draw v1, v2, 5

    load v1, 7
    load v2, 1
    load [I], ascii_O
    draw v1, v2, 5

    load v1, 13
    load v2, 1
    load [I], ascii_N
    draw v1, v2, 5

    load v1, 19
    load v2, 1
    load [I], ascii_E
    draw v1, v2, 5

    jmp inf

.font ascii_E
    " *****  "
    " *      "
    " *****  "
    " *      "
    " *****  "

.font ascii_R
    " *****  "
    " *   *  "
    " *****  "
    " ****   "
    " *   *  "

.font ascii_D
    " ****   "
    " *   *  "
    " *   *  "
    " *   *  "
    " ****   "

.font ascii_O
    " *****  "
    " *   *  "
    " *   *  "
    " *   *  "
    " *****  "

.font ascii_N
    " *   *  "
    " **  *  "
    " * * *  "
    " *  **  "
    " *   *  "