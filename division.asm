JMP    0x205
SNE    V3 0x38
SE     V0 V6
JMP    0x4a3
ADD    V0 0xf0
SE     V5 V6
4a30 ; HEX    0x4a30
LOAD   Vf 0xf0
SE     V5 V6
a300 ; HEX    0xa300
ADD    V1 0xf0
SE     V5 V10
ADD    V0 0xf0
LOAD   V5 0x85
a300 ; HEX    0xa300
LOAD   Vf 0xf0
LOAD   V5 0x81
8000 ; HEX    0x8000
SE     V0 V8
JMP    0x81
5810 ; HEX    0x5810
CALL   0x90
JMP    0x6f
3f00 ; HEX    0x3f00
1200 ; HEX    0x1200
bfa3 ; HEX    0xbfa3
ADD    V0 0xf0
LOAD   V5 0x85
6000 ; HEX    0x6000
1810 ; HEX    0x1810
8000 ; HEX    0x8000
SE     V0 V8
JMP    0x6a3
LOAD   Ve 0xf0
SE     V5 V10
LOAD   Vf 0xf0
LOAD   V5 0xa3
LOAD   Vd 0xf0
SE     V5 V6
1a30 ; HEX    0x1a30
LOAD   Vc 0xf0
SE     V5 V10
LOAD   Ve 0xf0
LOAD   V5 0x85
a300 ; HEX    0xa300
LOAD   Vd 0xf0
LOAD   V5 0x81
8000 ; HEX    0x8000
SE     V0 V8
JMP    0x81
5810 ; HEX    0x5810
CALL   0x90
JMP    0x6f
3f00 ; HEX    0x3f00
1200 ; HEX    0x1200
SNE    V5 V10
LOAD   Vd 0xf0
LOAD   V5 0x85
6000 ; HEX    0x6000
1810 ; HEX    0x1810
8000 ; HEX    0x8000
SE     V0 V8
JMP    0xea3
LOAD   Vd 0xf0
SE     V5 V10
LOAD   Vc 0xf0
LOAD   V5 0x85
6000 ; HEX    0x6000
1810 ; HEX    0x1810
8000 ; HEX    0x8000
SE     V0 V8
JMP    0xea3
LOAD   Vc 0xf0
SE     V5 V1
SE     V3 V10
ADD    V0 0xf0
LOAD   V5 0x85
a300 ; HEX    0xa300
LOAD   Vd 0xf0
LOAD   V5 0x81
8000 ; HEX    0x8000
SE     V0 V8
JMP    0x5a3
ADD    V0 0xf0
SE     V5 V10
ADD    V1 0xf0
LOAD   V5 0x85
a300 ; HEX    0xa300
LOAD   Vc 0xf0
LOAD   V5 0x81
8000 ; HEX    0x8000
SE     V0 V8
JMP    0x4a3
ADD    V1 0xf0
SE     V5 V1
JMP    0x760
8300 ; HEX    0x8300
6000 ; HEX    0x6000
8400 ; HEX    0x8400
a300 ; HEX    0xa300
ADD    V1 0xf0
LOAD   V5 0x23
SE     V1 V6
JMP    0x4a3
ADD    V0 0xf0
SE     V5 V6
4a30 ; HEX    0x4a30
LOAD   Vf 0xf0
SE     V5 V6
8300 ; HEX    0x8300
6000 ; HEX    0x6000
a840 ; HEX    0xa840
a300 ; HEX    0xa300
ADD    V0 0xf0
LOAD   V5 0x85
a300 ; HEX    0xa300
LOAD   Vf 0xf0
LOAD   V5 0x81
8000 ; HEX    0x8000
SE     V0 V2
JMP    0x323
SE     V1 V1
f381 ; HEX    0xf381
a300 ; HEX    0xa300
ADD    V2 0x62
18e0 ; HEX    0x18e0
CALL   0x5fe
JMP    0xef0
LOAD   V5 0x0
ee62 ; HEX    0xee62
1630 ; HEX    0x1630
8300 ; HEX    0x8300
4810 ; HEX    0x4810
CALL   0x531
1300 ; HEX    0x1300
7800 ; HEX    0x7800
SE     V0 0x0
eea3 ; HEX    0xeea3
ADD    V2 0xfe
JMP    0xef6
SE     V5 V6
8200 ; HEX    0x8200
8200 ; HEX    0x8200
JMP    0x53f
1130 ; HEX    0x1130
SE     Vf 0x83
8300 ; HEX    0x8300
6840 ; HEX    0x6840
JMP    0x65
1820 ; HEX    0x1820
SE     V0 0x82
SNE    V5 0x3f
1130 ; HEX    0x1130
SE     V9 0x84
e850 ; HEX    0xe850
e130 ; HEX    0xe130
CALL   0xb80
SNE    V5 0x86
SE     V4 V1
JMP    0xbf5
LOAD   V5 0x80
LOAD   V0 0x0
ee82 ; HEX    0xee82
8000 ; HEX    0x8000
JMP    0x53f
1300 ; HEX    0x1300
SNE    V5 0x80
CALL   0x0
eea3 ; HEX    0xeea3
LOAD   V9 0xf0
SE     V3 0xf2
LOAD   V5 0xf0
CALL   0x9d3
SNE    V5 0x73
6f10 ; HEX    0x6f10
CALL   0x9d3
SNE    V5 0x73
6f20 ; HEX    0x6f20
CALL   0x9d3
SNE    V5 0x0
ee28 ; HEX    0xee28
LOAD   V3 0x29
0x00 0x00; NOP
0x00 0x00; NOP
0x00 0x00; NOP
