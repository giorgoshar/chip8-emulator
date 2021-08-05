import os
import sys
from collections import namedtuple


filename = sys.argv[1]
rom = bytearray()
with open(filename, 'rb') as fileb:
    rom = bytearray(fileb.read())
pc = 0x0

print(f'addr | opcode | instruction')
print(f'{"-" * 40}')

while pc < len(rom) - 1:
    opcode = (rom[pc] << 8) | rom[pc + 1]
    
    op  = (opcode & 0xf000) >> 12
    x   = (opcode & 0x0f00) >> 8
    y   = (opcode & 0x00f0) >> 4
    n   =  opcode & 0x000f
    kk  =  opcode & 0x00ff
    nnn =  opcode & 0x0fff

    if   op == 0x0 and (opcode & 0xff) == 0xe0: print(f'{pc+0x200:<03x} | {opcode:<4x} | CLS')
    elif op == 0x0 and (opcode & 0xff) == 0xee: print(f'{pc+0x200:<03x} | {opcode:<4x} | RET')
    elif op == 0x1: print(f'{pc+0x200:<03x} | {opcode:<4x} | JP   0x{nnn:x}')
    elif op == 0x2: print(f'{pc+0x200:<03x} | {opcode:<4x} | CALL 0x{nnn:x}')
    elif op == 0x3: print(f'{pc+0x200:<03x} | {opcode:<4x} | SE   V{x:x} 0x{kk:x}')
    elif op == 0x4: print(f'{pc+0x200:<03x} | {opcode:<4x} | SNE  V{x:x} 0x{kk:x}')
    elif op == 0x5: print(f'{pc+0x200:<03x} | {opcode:<4x} | SE   V{x:x} V{y}')
    elif op == 0x6: print(f'{pc+0x200:<03x} | {opcode:<4x} | LD   V{x:x} 0x{kk:x}')
    elif op == 0x7: print(f'{pc+0x200:<03x} | {opcode:<4x} | ADD  V{x:x} 0x{kk:x}')
    elif op == 0x9: print(f'{pc+0x200:<03x} | {opcode:<4x} | SNE  V{x:x} V{y}')
    elif op == 0xa: print(f'{pc+0x200:<03x} | {opcode:<4x} | LD   [I] 0x{nnn:x}')
    elif op == 0xc: print(f'{pc+0x200:<03x} | {opcode:<4x} | RND  V{x:x} 0x{kk:x}')
    elif op == 0xd: print(f'{pc+0x200:<03x} | {opcode:<4x} | DRAW {x:x}, {y:x}, 0x{n:x}')   
    # ==[ input operation ]==
    elif op == 0xe and (opcode & 0xff) == 0x9e: print(f'{pc+0x200:<03x} | {opcode:<4x} | skp_pressed')
    elif op == 0xe and (opcode & 0xff) == 0xa1: print(f'{pc+0x200:<03x} | {opcode:<4x} | skp_not_pressed')  
    
    # ==[ logical operation ]==
    elif op == 0x8 and (opcode & 0xf) == 0x0: print(f'{pc+0x200:<03x} | {opcode:<4x} | LD   V{x:x} V{y:x}')
    elif op == 0x8 and (opcode & 0xf) == 0x1: print(f'{pc+0x200:<03x} | {opcode:<4x} | OR   V{x:x} V{y:x}')
    elif op == 0x8 and (opcode & 0xf) == 0x2: print(f'{pc+0x200:<03x} | {opcode:<4x} | AND  V{x:x} V{y:x}')
    elif op == 0x8 and (opcode & 0xf) == 0x3: print(f'{pc+0x200:<03x} | {opcode:<4x} | XOR  V{x:x} V{y:x}')
    elif op == 0x8 and (opcode & 0xf) == 0x4: print(f'{pc+0x200:<03x} | {opcode:<4x} | ADD  V{x:x} V{y:x}')
    elif op == 0x8 and (opcode & 0xf) == 0x5: print(f'{pc+0x200:<03x} | {opcode:<4x} | SUB  V{x:x} V{y:x}')
    elif op == 0x8 and (opcode & 0xf) == 0x6: print(f'{pc+0x200:<03x} | {opcode:<4x} | SHR  V{x:x} V{y:x}')
    elif op == 0x8 and (opcode & 0xf) == 0x7: print(f'{pc+0x200:<03x} | {opcode:<4x} | SUBN V{x:x} V{y:x}')
    elif op == 0x8 and (opcode & 0xf) == 0xe: print(f'{pc+0x200:<03x} | {opcode:<4x} | SHL  V{x:x} V{y:x}')  
    
    # ==[ subroutine operation ]==
    elif op == 0xf and (opcode & 0xff) == 0x07: print(f'{pc+0x200:<03x} | {opcode:<4x} | fx07(x)')
    elif op == 0xf and (opcode & 0xff) == 0x0a: print(f'{pc+0x200:<03x} | {opcode:<4x} | fx0a(x)')
    elif op == 0xf and (opcode & 0xff) == 0x55: print(f'{pc+0x200:<03x} | {opcode:<4x} | LD  [I], V{x:x}')
    elif op == 0xf and (opcode & 0xff) == 0x1e: print(f'{pc+0x200:<03x} | {opcode:<4x} | ADD [I] V{x:x}')
    elif op == 0xf and (opcode & 0xff) == 0x15: print(f'{pc+0x200:<03x} | {opcode:<4x} | fx15(x)')
    elif op == 0xf and (opcode & 0xff) == 0x18: print(f'{pc+0x200:<03x} | {opcode:<4x} | fx18(x)')
    elif op == 0xf and (opcode & 0xff) == 0x65: print(f'{pc+0x200:<03x} | {opcode:<4x} | LD  V{x:x} [I]')
    elif op == 0xf and (opcode & 0xff) == 0x29: print(f'{pc+0x200:<03x} | {opcode:<4x} | fx29(x)')
    elif op == 0xf and (opcode & 0xff) == 0x33: print(f'{pc+0x200:<03x} | {opcode:<4x} | fx33(x)')
    else: print(f'Unknown opcode: {opcode} at pc: {pc}')
    pc += 2
