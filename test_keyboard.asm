.org 0x200
jmp main
.var A 0x1
main:
    jmp keyboard

keyboard:
    load v3, 1 ; x position
    load v4, 1 ; y position

    sknp 0
    load [I], 0 ; default chip8 font `0`
    
    sknp 1
    load [I], 5 ; default chip8 font `1`

    sknp 2
    load [I], 10 ; default chip8 font `2`

    sknp 3
    load [I], 15 ; default chip8 font `3`
    
    sknp 4
    load [I], 20 ; default chip8 font `4`
    
    sknp 5
    load [I], 25 ; default chip8 font `5`

    sknp 15
    load [I], 75 ; default chip8 font `F`

    cls
    draw v3, v4, 5
    jmp keyboard