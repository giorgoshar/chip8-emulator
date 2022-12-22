__LABEL_Program:
JMP __LABEL_main
__LABEL_main:
CALL __LABEL_loop_cond
__LABEL_loop_cond:
LOAD v5, 0
LOAD v6, 50
__LABEL_loop:
LOAD vf, v6
SUBN vf v5
SNE vf 0
JMP __LABEL_end_if
LOAD v5, 0
LOAD v7, 7
LOAD v8, 8
__LABEL_end_if:
CALL __LABEL_drawnumber
ADD v5 5
JMP __LABEL_loop
RET
__LABEL_drawnumber:
CLS
LOAD va, 0
LOAD vb, 0
LOAD [I], 0
ADD [I] v5
DRAW va vb 5
RET
__LABEL_inf:
JMP __LABEL_inf
