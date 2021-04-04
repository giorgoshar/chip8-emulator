import sys
import os
import os.path

def disassemble(opcode):
    ins    = (opcode & 0xf000) >> 12
    x      = (opcode & 0x0f00) >> 8
    y      = (opcode & 0x00f0) >> 4
    nibble =  opcode & 0x000f
    kk     =  opcode & 0x00ff
    nnn    =  opcode & 0x0fff
    
    if   ins == 0x0 and opcode == 0x00e0: print('CLS')
    elif ins == 0x0 and opcode == 0x00ee: print('RET')

    elif ins == 0x1: print(f'JP   {hex(nnn)}')
    elif ins == 0x2: print(f'CALL {hex(nnn)}')
    elif ins == 0x3: print(f'SE   V{x}, {hex(kk)}')
    elif ins == 0x4: print(f'SNE  V{x}, {hex(kk)}')
    elif ins == 0x5: print(f'SE   V{x}, V{y}')
    elif ins == 0x6: print(f'LD   V{x}, {hex(kk)}')
    elif ins == 0x7: print(f'ADD  V{x}, {hex(kk)}')
    
    elif ins == 0x8 and (opcode & 0xf) == 0x0: print(f'LD   V{x}, V{y}')
    elif ins == 0x8 and (opcode & 0xf) == 0x1: print(f'OR   V{x}, V{y}')
    elif ins == 0x8 and (opcode & 0xf) == 0x2: print(f'AND  V{x}, V{y}')
    elif ins == 0x8 and (opcode & 0xf) == 0x3: print(f'XOR  V{x}, V{y}')
    elif ins == 0x8 and (opcode & 0xf) == 0x4: print(f'ADD  V{x}, V{y}')
    elif ins == 0x8 and (opcode & 0xf) == 0x5: print(f'SUB  V{x}, V{y}')
    elif ins == 0x8 and (opcode & 0xf) == 0x6: print(f'SHR  V{x}  [, V{y}]')
    elif ins == 0x8 and (opcode & 0xf) == 0x7: print(f'SUBN V{x}, V{y}')
    elif ins == 0x8 and (opcode & 0xf) == 0xe: print(f'SHL  V{x}  [, V{y}]')

    elif ins == 0x9: print(f'SNE  V{x}, V{y}')
    elif ins == 0xa: print(f'LD   I, {hex(nnn)}')
    elif ins == 0xe: print(f'SHL  V{x} [, V{y}]')
    elif ins == 0xc: print(f'RND  V{x} {hex(kk)}')
    elif ins == 0xd: print(f'DRW  V{x}, V{y}, {nibble}')

    elif ins == 0xf and (opcode & 0xff) == 0x07: print(f'LD   V{x},  DT')
    elif ins == 0xf and (opcode & 0xff) == 0x0a: print(f'LD   V{x},  K')
    elif ins == 0xf and (opcode & 0xff) == 0x15: print(f'LD   DT,  V{x}')
    elif ins == 0xf and (opcode & 0xff) == 0x18: print(f'LD   ST,  V{x}')
    elif ins == 0xf and (opcode & 0xff) == 0x1e: print(f'ADD I,   V{x}')
    elif ins == 0xf and (opcode & 0xff) == 0x29: print(f'LD   F,   V{x}')
    elif ins == 0xf and (opcode & 0xff) == 0x33: print(f'LD   B,   V{x}')
    elif ins == 0xf and (opcode & 0xff) == 0x55: print(f'LD   [I], V{x}')
    elif ins == 0xf and (opcode & 0xff) == 0x65: print(f'LD   V{x},  [I]')
    else: print('---')



if __name__ == '__main__':

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

    print(f'ROM len:{len(rom)}')
    print(f'| {"addr":<6} | {"opcode"} | instruction ')
    print('----------------------------------------')
    for pc in range(0, len(rom), 2):
        
        if pc + 1 >= len(rom):
            break

        opcode = (rom[pc] << 8) | (rom[pc + 1])
        print(f'| 0x{pc + 0x200:04x} | 0x{opcode:04x} | ', end='')
        disassemble(opcode)
    
