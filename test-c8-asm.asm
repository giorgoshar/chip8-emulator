__LABEL_Program:
JMP __LABEL_main
__LABEL_main:
LOAD v1, 1
LOAD v2, 2
ADD v1 v2
SNE v1 3
CALL __LABEL_drawSmile
__LABEL_inf:
JMP __LABEL_inf
__LABEL_drawSmile:
LOAD v1, 5
LOAD v2, 5
LOAD [I], l_SMILE
DRAW v1 v2 5
RET
.font l_SMILE 0x18 0x48 0x8 0x48 0x18, endfont
