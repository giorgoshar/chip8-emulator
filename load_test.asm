.org 0x200
jmp main
main:
    load v0 0
    load v1 0x50
    loop:

        load vf v1
        subn vf v0
        se   vf v0
        load v0 0
        add  v0 5
        jmp loop
inf: jmp inf