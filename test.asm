.org 0x200
jmp main

main:

loop:
    load [I], 0x230
    rand v1, 1
    rand v2, 2
    load [I], v2
    jmp  loop

inf: 
    jmp inf

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