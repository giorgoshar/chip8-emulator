.org   0x200
jmp    main
.ascii  "GREET.ASM, Copyright 2014 Boro Sitnikovski"
main:
SMILE:
    load    v1, 28        ; x position
    load    v2, 5         ; y position
    load    [I], l_SMILE  ; draw smile picture
    draw    v1, v2, 5     ; draw
loop:
    jmp     loop

.font l_SMILE
   "    *   ",
   "  *  *  ",
   "     *  ",
   "  *  *  ",
   "    *   "
.font l_SAD
    "      * ",
    "  *  *  ",
    "     *  ",
    "  *  *  ",
    "      * "