.org   0x200
jmp    main
.ascii  "GREET.ASM, Copyright 2014 Boro Sitnikovski"
main:

SMILE:
    ; x position
    load    v1, 5

    ; y position
    load    v2, 5     

    ; load font    
    load    [I], l_SMILE

    ; draw
    draw    v1, v2, 5
loop:
    jmp     loop

.font l_SMILE 0x18 0x48 0x08 0x48 0x18, endfont
.font l_SAD   0x18 0x50 0x10 0x50 0x18, endfont