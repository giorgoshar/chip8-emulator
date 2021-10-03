.org 0x200
jmp main
; .var A 0x1
main:
    jmp  DrawGrid

inf: jmp inf

DrawGrid:
    load v0, 0 ; x position
    load v1, 0 ; y position
    load [I], GRID
    draw v0, v1, 8
    jmp inf

err:
    load v1, 1
    load v2, 1
    load [I], letter_E
    draw v1, v2, 5

    load v1, 7
    load v2, 1
    load [I], letter_R
    draw v1, v2, 5

    load v1, 13
    load v2, 1
    load [I], letter_R
    draw v1, v2, 5
    
    jmp inf
done:
    load v1, 1
    load v2, 1
    load [I], letter_D
    draw v1, v2, 5

    load v1, 7
    load v2, 1
    load [I], letter_O
    draw v1, v2, 5

    load v1, 13
    load v2, 1
    load [I], letter_N
    draw v1, v2, 5

    load v1, 19
    load v2, 1
    load [I], letter_E
    draw v1, v2, 5

    jmp inf
.font letter_A 0x1c 0x22 0x3e 0x22 0x22, endfont
.font letter_E 0x7c 0x40 0x7c 0x40 0x7c, endfont
.font letter_R 0x7c 0x44 0x7c 0x78 0x44, endfont
.font letter_D 0x78 0x44 0x44 0x44 0x78, endfont
.font letter_O 0x7c 0x44 0x44 0x44 0x7c, endfont
.font letter_N 0x44 0x64 0x54 0x4c 0x44, endfont

; 0xAA = 1010 1010
; 0x55 = 0101 0101
.font GRID  
    0xAA ; line 1
    0x55 ; line 2
    0xAA ; line 3
    0x55 ; line 4
    0xAA ; line 5
    0x55 ; line 6
    0xAA ; line 7
    0x55 ; line 8
endfont
