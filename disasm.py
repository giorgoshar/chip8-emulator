import sys
import os
import os.path

os.system("clear")

if len(sys.argv) != 2:
    print('Please provider file path')
    sys.exit()

if not os.path.isfile(sys.argv[1]):
    print('File doesn\'t exist')
    sys.exit()

filename = sys.argv[1] # './GREET'
rom = bytearray([0] * 4096)
with open(filename, 'rb') as fp:
    rom = bytearray(fp.read())

print(f'| {"addr":<6} | {"opcode"} | instruction ')
print('----------------------------------------')
idx = 0

for idx in range(0, len(rom), 2):
    
    if idx + 1 >= len(rom):
        break

    opcode    = (rom[idx] << 8) | (rom[idx + 1])
    operation = (opcode & 0xf000) >> 12
    x         = (opcode & 0x0f00) >> 8
    y         = (opcode & 0x00f0) >> 4
    nibble    =  opcode & 0x000f
    kk        =  opcode & 0x00ff
    nnn       =  opcode & 0x0fff

    print(f'| 0x{idx:04x} | 0x{opcode:04x} | ', end='')
    if operation == 0x0:
        if opcode == 0x0000: print('CLS')
        if opcode == 0x00ee: print('RET')
        else: sys.exit(f'fail opcode: 0x{opcode:x}')
    elif operation == 0x1: print(f'JP   0x{nnn:x}')
    elif operation == 0x2: print(f'CALL 0x{nnn:x}')
    elif operation == 0x3: print(f'SE   V{x}, 0x{kk:x}')
    elif operation == 0x4: print(f'SNE  V{x}, 0x{kk:x}')
    elif operation == 0x5: print(f'SE   V{x}, V{y}')
    elif operation == 0x6: print(f'LD   V{x}, 0x{kk:x}')
    elif operation == 0x7: print(f'ADD  V{x}, {kk:x}')
    elif operation == 0x8:
        lo_op = opcode & 0xf
        if   lo_op == 0x0: print(f'LD   V{x}, V{y}')
        elif lo_op == 0x1: print(f'OR   V{x}, V{y}')
        elif lo_op == 0x2: print(f'AND  V{x}, V{y}')
        elif lo_op == 0x3: print(f'XOR  V{x}, V{y}')
        elif lo_op == 0x4: print(f'ADD  V{x}, V{y}')
        elif lo_op == 0x5: print(f'SUB  V{x}, V{y}')
        elif lo_op == 0x6: print(f'SHR  V{x}  [, V{y}]')
        elif lo_op == 0x7: print(f'SUBN V{x}, V{y}')
        elif lo_op == 0xe: print(f'SHL  V{x}  [, V{y}]')
        else: sys.exit(f'fail lo_op: 0x{lo_op:x}')
    elif operation == 0x9: print(f'SNE  V{x}, V{y}')
    elif operation == 0xa: print(f'LD   I, 0x{nnn:x}')
    elif operation == 0xe: print(f'SHL  V{x} [, V{y}]')
    elif operation == 0xc: print(f'RND  V{x} {kk:x}')
    elif operation == 0xd: print(f'DRW  V{x}, V{y}, {nibble:x}')
    elif operation == 0xf:
        subroutine_op = opcode & 0xff
        if   subroutine_op == 0x07: print(f'LD   V{x},  DT')
        elif subroutine_op == 0x0a: print(f'LD   V{x},  K')
        elif subroutine_op == 0x15: print(f'LD   DT,  V{x}')
        elif subroutine_op == 0x18: print(f'LD   ST,  V{x}')
        elif subroutine_op == 0x1e: print(f'ADD I,   V{x}')
        elif subroutine_op == 0x29: print(f'LD   F,   V{x}')
        elif subroutine_op == 0x33: print(f'LD   B,   V{x}')
        elif subroutine_op == 0x55: print(f'LD   [I], V{x}')
        elif subroutine_op == 0x65: print(f'LD   V{x},  [I]')
        else: sys.exit(f'fail subroutine: 0x{subroutine_op:x}')
    else: sys.exit(f'fail operation: 0x{operation:x}')

