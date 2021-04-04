# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=unused-import

import sys
import os.path
import numpy
import pygame

from devices.CPU      import CPU
from devices.Memory   import Memory
from devices.Display  import Display
from devices.Keyboard import Keyboard

import disasm

pygame.init()
screen  = pygame.display.set_mode([500, 500])

class Chip8:
    def __init__(self):

        self.memory   = Memory(4096)
        self.cpu      = CPU()
        self.video    = Display(screen)
        self.keyboard = Keyboard()

        self.fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]

    def load(self, filename):
        self.reset()
        with open(filename, 'rb') as fp:
            rom = fp.read()
        
        # load rom to memory
        for offset, byte in enumerate(rom):
            self.memory.write(0x200 + offset, byte)

        # load fonts
        for i in range(0, len(self.fontset)):
            self.memory.write(i, self.fontset[i])

    def reset(self):
        self.cpu  = CPU()
        self.memory = Memory(4096)
        self.video.clear()
        self.keyboard.reset()

    def run(self):
        # clock = pygame.time.Clock()
        running = True
        while running:
            # clock.tick(60)

            self.keyboard.handle()

            self.cpu.opcode = (self.memory.read(self.cpu.pc) << 8) | self.memory.read(self.cpu.pc + 1)
            self.execute(self.cpu.opcode)

            if self.cpu.timer['delay'] > 0: 
                self.cpu.timer['delay'] -= 1
            if self.cpu.timer['sound'] > 0: 
                self.cpu.timer['sound'] -= 1
            
            self.video.render()
            pygame.display.flip()

    def execute(self, opcode):

        operation = (opcode & 0xf000) >> 12
        x    = (opcode & 0x0f00) >> 8
        y    = (opcode & 0x00f0) >> 4
        n    =  opcode & 0x000f
        kk   =  opcode & 0x00ff
        nnn  =  opcode & 0x0fff

        self.cpu.pc += 2
        # disasm.disassemble(opcode)
        
        # ==[ main operations ]==
        if   operation == 0x0: self.CLS_RET(opcode)
        elif operation == 0x1: self.JP(nnn)
        elif operation == 0x2: self.CALL(nnn)
        elif operation == 0x3: self.SE_Vx_kk(x, kk)
        elif operation == 0x4: self.SNE_Vx_kk(x, kk)
        elif operation == 0x5: self.SE_Vx_Vy(x, y)
        elif operation == 0x6: self.LD_VX(x, kk)
        elif operation == 0x7: self.ADD_VX(x, kk)
        elif operation == 0x9: self.SNE_Vx_Vy(x, y)
        elif operation == 0xa: self.LD_I(nnn)
        elif operation == 0xc: self.RND(x, kk)
        elif operation == 0xd: self.DRAW(x, y, n)

        # ==[ input operations ]==
        elif operation == 0xe and (opcode & 0xff) == 0x9e: self.skp_pressed(x)
        elif operation == 0xe and (opcode & 0xff) == 0xa1: self.skp_not_pressed(x)

        # ==[ logical operations ]==
        elif operation == 0x8 and (opcode & 0xf) == 0x0: self.lo_ld(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0x1: self.lo_or(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0x2: self.lo_and(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0x3: self.lo_xor(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0x4: self.lo_add(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0x5: self.lo_sub(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0x6: self.lo_shr(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0x7: self.lo_subn(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0xe: self.lo_shl(x, y)

        # ==[ subroutine operations ]==
        elif operation == 0xf and (opcode & 0xff) == 0x07: self.fx07(x)
        elif operation == 0xf and (opcode & 0xff) == 0x0a: self.fx0a(x)
        elif operation == 0xf and (opcode & 0xff) == 0x55: self.fx55(x)
        elif operation == 0xf and (opcode & 0xff) == 0x1e: self.fx1e(x)
        elif operation == 0xf and (opcode & 0xff) == 0x15: self.fx15(x)
        elif operation == 0xf and (opcode & 0xff) == 0x18: self.fx18(x)
        elif operation == 0xf and (opcode & 0xff) == 0x65: self.fx65(x)
        elif operation == 0xf and (opcode & 0xff) == 0x29: self.fx29(x)
        elif operation == 0xf and (opcode & 0xff) == 0x33: self.fx33(x)
        
        # Super Chip-48 Instructions
        elif operation == 0xf and (opcode & 0xff) == 0x75: sys.exit('super chip8 not implemented')
        elif operation == 0xf and (opcode & 0xff) == 0x85: sys.exit('super chip8 not implemented')
        else: sys.exit(f'(???) Failed to execute opcode: {hex(opcode)}, operation:{hex(operation)} {hex(opcode & 0xff)}')

    # -- BEGIN INPUT HANDLE --
    def skp_pressed(self, x):
        if self.keyboard.keypad[x] == 1:
            self.cpu.pc += 2
    def skp_not_pressed(self, x):
        if self.keyboard.keypad[x] == 0:
            self.cpu.pc += 2

    # -- BEGIN Logical Operatios
    def lo_ld(self, x, y):
        self.cpu.v[x] = self.cpu.v[y]
    def lo_or(self, x, y):
        self.cpu.v[x] |= self.cpu.v[y]
    def lo_shr(self, x, y):
        self.cpu.v[0xF] = self.cpu.v[x] & 0x1
        self.cpu.v[x] = (self.cpu.v[x] >> 1) & 0xff
    def lo_shl(self, x, y):
        self.cpu.v[0xF] = self.cpu.v[x] >> 7
        self.cpu.v[x] = (self.cpu.v[x] << 1) & 0xff
    def lo_add(self, x, y):
        print(x, y, self.cpu.v[x] , self.cpu.v[y])
        if (self.cpu.v[x] + self.cpu.v[y]) > 0xff:
            self.cpu.v[0xf] = 1
        else:
            self.cpu.v[0xf] = 0
        self.cpu.v[x] = (self.cpu.v[x] + self.cpu.v[y]) & 0xff
    def lo_xor(self, x, y):
        self.cpu.v[x] ^= self.cpu.v[y]
    def lo_and(self, x, y):
        self.cpu.v[x] &= self.cpu.v[y]
    def lo_sub(self, x, y):
        if self.cpu.v[x] >= self.cpu.v[y]:
            self.cpu.v[0xf] = 1
        else:
            self.cpu.v[0xf] = 0
        self.cpu.v[x] = (self.cpu.v[x] - self.cpu.v[y]) & 0xff
    def lo_subn(self, x, y):
        if self.cpu.v[y] >= self.cpu.v[x]:
            self.cpu.v[0xf] = 1
        else:
            self.cpu.v[0xf] = 0
        self.cpu.v[x] = (self.cpu.v[y] - self.cpu.v[x]) & 0xff

    # -- BEGIN Subroutine Operations
    def fx33(self, x): # BCD
        self.memory.write(self.cpu.i + 0, self.cpu.v[x] // 100)
        self.memory.write(self.cpu.i + 1, self.cpu.v[x] % 100 // 10)
        self.memory.write(self.cpu.i + 2, self.cpu.v[x] % 10)
    def fx15(self, x):
        self.cpu.timer['delay'] = self.cpu.v[x]
    def fx18(self, x):
        self.cpu.timer['sound'] = self.cpu.v[x]
    def fx0a(self, x):
        # wait for key to pressed
        pressed = False
        while not pressed:
            self.keyboard.handle()
            for key in range(0, len(self.keyboard.keypad)):
                if self.keyboard.keypad[key] == 0x1:
                    self.cpu.v[x] = key
                    pressed = True
    def fx07(self, x):
        self.cpu.v[x] = self.cpu.timer['delay']
    def fx29(self, x):
        self.cpu.i = (self.cpu.v[x] * 0x5) & 0xff
    def fx1e(self, x):
        self.cpu.i += self.cpu.v[x]
    def fx55(self, x):
        for counter in range(0, x + 1):
            self.memory.write(self.cpu.i + counter, self.cpu.v[counter])
    def fx65(self, x):
        for counter in range(0, x + 1):
            self.cpu.v[counter] = self.memory.read(self.cpu.i + counter)
    # -- END  Subroutine Operations

    def RND(self, x, kk):
        rnd = numpy.random.randint(0x0, 0xff)
        self.cpu.v[x] = rnd & kk

    def JP(self, nnn):
        if nnn == 0x450:
            self.cpu.dump()
            input()
        self.cpu.pc = nnn

    def ADD_VX(self, x, kk):
        self.cpu.v[x] = (self.cpu.v[x] + kk) & 0xff

    def DRAW(self, x, y, nibble):
        locX = self.cpu.v[x]
        locY = self.cpu.v[y]
        self.cpu.v[0xf] = 0x0
        for row in range(0, nibble):
            sprite = self.memory.read(self.cpu.i  + row)
            for col in range(0, 8):
                if (sprite & 0x80) > 0:
                    screenY = (locY + row) % self.video.rows
                    screenX = (locX + col) % self.video.cols
                    if self.video.buffer[ screenY ][ screenX ] == 1:
                        self.cpu.v[0xf] = 0x1
                    self.video.buffer[ screenY ][ screenX ] ^= 1
                sprite <<= 1

    def SE_Vx_kk(self, x, kk):
        if self.cpu.v[x] == kk:
            self.cpu.pc += 2

    def SE_Vx_Vy(self, x, y):
        if self.cpu.v[x] == self.cpu.v[y]:
            self.cpu.pc += 2

    def CALL(self, nnn):
        self.cpu.stack[ self.cpu.sp ] = self.cpu.pc
        self.cpu.sp += 1
        self.cpu.pc = nnn

    def LD_I(self, nnn):
        self.cpu.i = nnn

    def SNE_Vx_kk(self, x, kk):
        if self.cpu.v[x] != kk:
            self.cpu.pc += 2

    def SNE_Vx_Vy(self, x, y):
        if self.cpu.v[x] != self.cpu.v[y]:
            self.cpu.pc += 2

    def CLS_RET(self, opcode):
        # CLS
        if opcode == 0x0000:
            self.video.clear()
        # RET
        if opcode == 0x00ee:
            self.cpu.pc = self.cpu.stack[ self.cpu.sp - 1 ]
            self.cpu.sp -= 1

    def LD_VX(self, x, kk):
        self.cpu.v[x] = kk

chip8 = Chip8()
# romname = "./ROMS/KALEID"
# romname = "./ROMS/PUZZLE"
# romname = "./ROMS/test_opcode.ch8"
# romname = "./ROMS/IBM"
# romname = "./ROMS/BC_TEST"
# romname = "./ROMS/MISSILE"
# romname = "./ROMS_TEST/test_opcode.ch8"

if len(sys.argv) == 2:
    if os.path.isfile(sys.argv[1]):
        romname = sys.argv[1]
    else:
        sys.exit(f'[__ERROR__] file {sys.argv[1]} doesnt exist')


chip8.load(romname)
chip8.run()
