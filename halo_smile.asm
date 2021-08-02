.org   0x200
jmp    start
.ascii  "GREET.ASM, Copyright 2014 Boro Sitnikovski"
start:
HALO:
    load    v1, 0
    load    v2, 0x5
    ; add   v2, 1
    load    [I], l_H        
    draw    v1, v2, 5     
    load    v1, 6
    load    v2, 5
    load    [I], l_A
    draw    v1, v2, 5
    load    v1, 12
    load    v2, 5
    load    [I], l_L
    draw    v1, v2, 5
    load    v1, 18
    load    v2, 5
    load    [I], l_O
    draw    v1, v2, 5
SMILE:
    load    v1, 28        ; x position
    load    v2, 5         ; y position
    load    [I], l_SMILE  ; draw smile picture
    draw    v1, v2, 5     ; draw
loop:
    jmp     loop
l_SMILE:
    .pic    "    *   ",
            "  *  *  ",
            "     *  ",
            "  *  *  ",
            "    *   "
l_H:
    .pic    "   * *  ",
            "   * *  ",
            "   ***  ",
            "   * *  ",
            "   * *  "
l_A:
    .pic    "   ***  ",
            "   * *  ",
            "   ***  ",
            "   * *  ",
            "   * *  "
l_L:
    .pic    "   *    ",
            "   *    ",
            "   *    ",
            "   *    ",
            "   ***  "
l_O:
    .pic    "   ***  ",
            "   * *  ",
            "   * *  ",
            "   * *  ",
            "   ***  "
