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

from Display import Display
from Memory  import Memory

pygame.init()
screen = pygame.display.set_mode([500, 500])

class CPU:
    def __init__(self):
        self.v   = bytearray([0] * 16)
        self.i   = 0
        self.sp  = 0
        self.pc  = 0x200
        self.opcode = 0x0

        self.stack  = bytearray([0] * 16)
        self.timer = {
            'delay' : 0,
            'sound' : 0
        }

    def dump(self):
        print(
            f'============[ CPU REGISTERS ]============\n'
            f'v: {[hex(b) for b in self.v]}\n'
            f'i: {hex(self.i)}\n'
            f'pc: {hex(self.pc)}\n'
            f'sp: {hex(self.sp)}\n'
            f'stack: {[hex(b) for b in self.stack]}\n'
            f'delay: {self.timer["delay"]}\n'
            f'sound: {self.timer["sound"]}\n'
            f'============[ INSTRUCTION ]============\n'
            f'opcode   : {hex( self.opcode)}\n'
            f'operation: {hex((self.opcode & 0xf000) >> 12)}\n'
            f'x        : {hex((self.opcode & 0x0f00) >> 8)}\n'
            f'y        : {hex((self.opcode & 0x00f0) >> 4)}\n'
            f'nibble   : {hex( self.opcode & 0x000f)}\n'
            f'kk       : {hex( self.opcode & 0x00ff)}\n'
            f'nnn      : {hex( self.opcode & 0x0fff)}'
        )

class Chip8:
    def __init__(self):
        self.memory  = Memory()
        self.cpu     = CPU()
        self.video   = Display(screen)

        self.keypad  = bytearray([0] * 16)
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

        self.dbg = False
        self.opcode = 0x0

        # self.instructions = {
        #     0x0000: self.op_0nnn,
        #     0x1000: self.op_1nnn
        # }

    def load(self, filename):
        self.reset()
        with open(filename, 'rb') as fp:
            rom = bytearray(fp.read())
        
        # load rom to memory
        for offset, byte in enumerate(rom):
            self.memory.write(0x200 + offset, byte)

        # load fonts
        for i in range(0, len(self.fontset)):
            self.memory.write(i, self.fontset[i])

    def reset(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.video.clear()

    def tick(self):
        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.keypad[0x0] = 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_e:
                        self.keypad[0x0] = 0

            self.opcode = (self.memory.read(self.cpu.pc) << 8) | self.memory.read(self.cpu.pc + 1)
            if self.dbg:
                self.cpu.dump()

            try: 
                self.execute(self.opcode)
            except (NotImplementedError, ValueError) as e:
                self.cpu.dump()
                print(e)
                sys.exit()

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

        if   operation == 0x0: self.CLS_RET(opcode)
        elif operation == 0x1: self.JP(nnn)
        elif operation == 0x2: self.CALL(nnn)
        elif operation == 0x3: self.SE(x, kk)
        elif operation == 0x4: self.SNE(x, kk)
        elif operation == 0x5: self.SE_Vx_Vy(x, y)
        elif operation == 0x6: self.LD_VX(x, kk)
        elif operation == 0x7: self.ADD_VX(x, kk)

        elif operation == 0xa: self.LD_I(nnn)
        elif operation == 0xc: self.RND(x, kk)
        elif operation == 0xd: self.DRAW(x, y, n)

        # ==[ inputs ]==
        elif operation == 0xe and (opcode & 0xff) == 0x9e: self.skp_pressed(x)
        elif operation == 0xe and (opcode & 0xff) == 0xa1: self.skp_not_pressed(x)

        # ==[ logical instructions ]==
        elif operation == 0x8 and (opcode & 0xf) == 0x0: self.lo_ld(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0x1: self.lo_or(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0x2: self.lo_and(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0x3: self.lo_xor(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0x5: self.lo_sub(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0x7: self.lo_subn(x, y)
        elif operation == 0x8 and (opcode & 0xf) == 0xe: self.lo_shl(x, y)

        # ==[ subroutine instructions ]==
        elif operation == 0xf and (opcode & 0xff) == 0x7 : self.fx07(x)
        elif operation == 0xf and (opcode & 0xff) == 0x0a: self.fx0a(x)
        elif operation == 0xf and (opcode & 0xff) == 0x55: self.fx55(x)
        elif operation == 0xf and (opcode & 0xff) == 0x1e: self.fx1e(x)
        elif operation == 0xf and (opcode & 0xff) == 0x15: self.fx15(x)
        elif operation == 0xf and (opcode & 0xff) == 0x18: self.fx18(x)
        elif operation == 0xf and (opcode & 0xff) == 0x65: self.fx65(x)
        elif operation == 0xf and (opcode & 0xff) == 0x29: self.fx29(x)
        elif operation == 0xf and (opcode & 0xff) == 0x33: self.fx33(x)
        else: raise NotImplementedError(f'(???) Failed to execute opcode: {hex(opcode)}')



    # -- BEGIN INPUT HANDLE --
    def skp_pressed(self, x):
        if self.keypad[0x0] == 1:
            self.cpu.pc += 2
        print(f'SKP V{x}')

    def skp_not_pressed(self, x):
        if self.keypad[0x0] == 0:
            self.cpu.pc += 2
        print(f'SKNP V{x}')

    # -- BEGIN Logical Operatios
    def lo_shl(self, x, y):
        self.cpu.v[0xf] = (self.cpu.v[x] & 0x80) >> 7
        self.cpu.v[x] <<= 1
        print(f'SHL V{x} [, V{y}]')
    def lo_xor(self, x, y):
        self.cpu.v[x] ^= self.cpu.v[y]
        print(f'XOR V{x}, V{y}')
    def lo_or(self, x, y):
        self.cpu.v[x] |= self.cpu.v[y]
        print(f'OR V{x}, V{y}')
    def lo_and(self, x, y):
        self.cpu.v[x] &= self.cpu.v[y]
        print(f'AND V{x}, V{y}')
    def lo_ld(self, x, y):
        self.cpu.v[x] = self.cpu.v[y]
        print(f'LD V{x}, V{y}')
    def lo_sub(self, x, y):
        if self.cpu.v[x] > self.cpu.v[y]:
            self.cpu.v[0xf] = 1
        else:
            self.cpu.v[0xf] = 0
        print(f'SUB V{x}, V{y}')
    def lo_subn(self, x, y):
        if self.cpu.v[y] > self.cpu.v[x]:
            self.cpu.v[0xf] = 1
        else:
            self.cpu.v[0xf] = 0
        print(f'SUBN V{x}, V{y}')
    # -- END   Logical Operatios

    # -- BEGIN Subroutine Operations
    def fx33(self, x):
        # sys.exit('[__ERROR__] Instruction function fx33')
        self.memory.write(self.cpu.i    , self.cpu.v[x] / 100)
        self.memory.write(self.cpu.i + 1, self.cpu.v[x] % 10 / 10)
        self.memory.write(self.cpu.i + 2, self.cpu.v[x] % 10)
        print(f'LD B, V{x}')

    def fx15(self, x):
        self.cpu.timer['delay'] = self.cpu.v[x]
        print(f'LD DT, V{x}')

    def fx18(self, x):
        self.cpu.timer['sound'] = self.cpu.v[x]
        print(f'LD ST, V{x}')

    def fx0a(self, x):
        sys.exit('[__ERROR__] fx0a')
        print(f'LD V{x}, K')

    def fx07(self, x):
        self.cpu.v[x] = self.cpu.timer['delay']
        print(f'LD V{x}, DT')

    def fx29(self, x):
        self.cpu.i = self.cpu.v[x] * 0x5
        print(f'LD I, V{x}')

    def fx65(self, x):
        for counter in range(0, x):
            self.cpu.v[counter] = self.memory.read(self.cpu.i + counter)
            print(f'LD V{x}, [{self.cpu.i + counter}]')

    def fx1e(self, x):
        self.cpu.i += self.cpu.v[x]
        print(f'ADD {hex(self.cpu.i)}, V{x}')

    def fx55(self, x):
        for counter in range(0, x):
            self.memory.write(self.cpu.i + counter, self.cpu.v[counter])
            print(f'LD [{hex(self.cpu.i)}], V{x}')
    # -- END  Subroutine Operations

    def SK_IF_PRESS(self, x):
        isPressed = self.keypad[ self.cpu.v[x] ]
        if isPressed == 0:
            self.cpu.pc += 2 

    def RND(self, x, kk):
        rnd = numpy.random.randint(0x0, 0xff)
        self.cpu.v[x] = rnd & kk
        print(f'RND V{x} {hex(rnd)}')

    def JP(self, nnn):
        self.cpu.pc = nnn
        print(f'JP {hex(nnn)}')

    def ADD_VX(self, x, kk):
        self.cpu.v[x] += kk
        print(f'ADD V{x}, {hex(kk)}')

    def DRAW(self, x, y, nibble):
        locX = self.cpu.v[x]
        locY = self.cpu.v[y]
        self.cpu.v[0xf] = 0x0
        for row in range(0, nibble):
            pixel = self.memory.read(self.cpu.i  + row)
            for col in range(0, 8):
                if (pixel & 0x80) > 0:
                    screenY = locY + row
                    screenX = locX + col
                    self.video.buffer[ screenY ][ screenX ] ^= pixel
                    if self.video.buffer[ screenY ][ screenX ] != 0:
                        self.cpu.v[0xf] = 0x1
                pixel = pixel << 1
        print(f'DRW V{hex(x)}, V{hex(x)}, {hex(nibble)}')       

    def SE(self, x, kk):
        if self.cpu.v[x] == kk:
            self.cpu.pc += 2
        print(f'SE V{x}, {hex(kk)}')

    def SE_Vx_Vy(self, x, y):
        if self.cpu.v[x] == self.cpu.v[y]:
            self.cpu.pc += 2
        print(f'SE V{x}, V{y}')

    def CALL(self, nnn):
        self.memory.write(self.cpu.sp, self.cpu.pc & 0x00ff)
        self.cpu.sp += 1
        self.memory.write(self.cpu.sp, (self.cpu.pc & 0xff00) >> 8)
        self.cpu.sp += 1
        self.cpu.pc = nnn
        print(f'CALL {hex(self.cpu.pc)}')

    def LD_I(self, nnn):
        self.cpu.i = nnn
        print(f'LD I, {hex(nnn)}')

    def SNE(self, x, kk):
        if self.cpu.v[x] != kk:
            self.cpu.pc += 2
        print(f'SNE {hex(self.cpu.v[x])}, {hex(kk)}')

    def CLS_RET(self, opcode):
        # CLS
        if opcode == 0x0000:
            self.video.clear()
            print('CLS')
        # RET
        if opcode == 0x000E:
            self.cpu.pc = self.cpu.stack[ self.cpu.sp ]
            print('RET')

    def LD_VX(self, x, kk):
        self.cpu.v[x] = kk
        print(f'LD V{x}, {hex(kk)}')

chip8 = Chip8()
# filename = "./ROMS/KALEID"
# filename = "./ROMS/PUZZLE"
# filename = "./ROMS/test_opcode.ch8"
# filename = "./ROMS/IBM"
# filename = "./ROMS/BC_TEST"
# filename = "./ROMS/MISSILE"
filename = "./ROMS/GREET"


if len(sys.argv) == 2:
    if os.path.isfile(sys.argv[1]):
        filename = sys.argv[1]
    else:
        sys.exit(f'[__ERROR__] file {sys.argv[1]} doesnt exist')


chip8.load(filename)
chip8.tick()

