import os
import sys

def disasm(opcode):
    ins = (opcode & 0xf000) >> 12
    x   = (opcode & 0x0f00) >> 8
    y   = (opcode & 0x00f0) >> 4
    n   =  opcode & 0x000f
    kk  =  opcode & 0x00ff
    nnn =  opcode & 0x0fff

    if   ins == 0x0 and (opcode & 0xff) == 0xe0: return "CLS"
    elif ins == 0x0 and (opcode & 0xff) == 0xee: return "RET"
    elif ins == 0x1: dissasmStr = f'JMP    0x{nnn:x}'
    elif ins == 0x2: dissasmStr = f'CALL   0x{nnn:x}'
    elif ins == 0x3: dissasmStr = f'SE     V{x:x} 0x{kk:x}'
    elif ins == 0x4: dissasmStr = f'SNE    V{x:x} 0x{kk:x}'
    elif ins == 0x5: dissasmStr = f'SE     V{x:x} V{y}'
    elif ins == 0x6: dissasmStr = f'LOAD   V{x:x} 0x{kk:x}'
    elif ins == 0x7: dissasmStr = f'ADD    V{x:x} 0x{kk:x}'
    elif ins == 0x9: dissasmStr = f'SNE    V{x:x} V{y}'
    elif ins == 0xa: dissasmStr = f'LOAD   [I] 0x{nnn:x}'
    elif ins == 0xc: dissasmStr = f'RAND   V{x:x} 0x{kk:x}'
    elif ins == 0xd: dissasmStr = f'DRAW   V{x:x} V{y:x} 0x{n:x}'
    
    # ==[ input operation ]==
    elif ins == 0xe and (opcode & 0xff) == 0x9e: dissasmStr = f'SKP    V{x:x}'
    elif ins == 0xe and (opcode & 0xff) == 0xa1: dissasmStr = f'SKNP   V{x:x}'
    
    # ==[ logical operation ]==
    elif ins == 0x8 and (opcode & 0xf) == 0x0: dissasmStr = f'LOAD   V{x:x} V{y:x}'
    elif ins == 0x8 and (opcode & 0xf) == 0x1: dissasmStr = f'OR     V{x:x} V{y:x}'
    elif ins == 0x8 and (opcode & 0xf) == 0x2: dissasmStr = f'AND    V{x:x} V{y:x}'
    elif ins == 0x8 and (opcode & 0xf) == 0x3: dissasmStr = f'XOR    V{x:x} V{y:x}'
    elif ins == 0x8 and (opcode & 0xf) == 0x4: dissasmStr = f'ADD    V{x:x} V{y:x}'
    elif ins == 0x8 and (opcode & 0xf) == 0x5: dissasmStr = f'SUB    V{x:x} V{y:x}'
    elif ins == 0x8 and (opcode & 0xf) == 0x6: dissasmStr = f'SHR    V{x:x} V{y:x}'
    elif ins == 0x8 and (opcode & 0xf) == 0x7: dissasmStr = f'SUBN   V{x:x} V{y:x}'
    elif ins == 0x8 and (opcode & 0xf) == 0xe: dissasmStr = f'SHL    V{x:x} V{y:x}'
    
    # ==[ subroutine operation ]=>0
    elif ins == 0xf and (opcode & 0xff) == 0x07: dissasmStr = f'LOAD   V{x:x}, DT'
    elif ins == 0xf and (opcode & 0xff) == 0x0a: dissasmStr = f'LOAD   V{x:x},  K'
    elif ins == 0xf and (opcode & 0xff) == 0x55: dissasmStr = f'LOAD   [I], V{x:x}'
    elif ins == 0xf and (opcode & 0xff) == 0x1e: dissasmStr = f'ADD    [I], V{x:x}'
    elif ins == 0xf and (opcode & 0xff) == 0x15: dissasmStr = f'LOAD   DT,  V{x:x}'
    elif ins == 0xf and (opcode & 0xff) == 0x18: dissasmStr = f'LOAD   ST,  V{x:x}'
    elif ins == 0xf and (opcode & 0xff) == 0x65: dissasmStr = f'LOAD   V{x:x}, [I]'
    elif ins == 0xf and (opcode & 0xff) == 0x29: dissasmStr = f'LOAD   F,  V{x:x}'
    elif ins == 0xf and (opcode & 0xff) == 0x33: dissasmStr = f'LOAD   B,  V{x:x}'
    else: dissasmStr = f'HEX    0x{opcode:<04x}'
    return dissasmStr

if __name__ == '__main__':
    filename = sys.argv[1]
    rom = bytearray()
    with open(filename, 'rb') as fileb:
        rom = bytearray(fileb.read())
    
    pc = 0x0
    while pc < len(rom):
        opcode = (rom[pc] << 8) | rom[pc + 1]
        instr  = disasm(opcode)
        print(hex(pc + 0x200), hex(opcode), instr)
        pc += 2