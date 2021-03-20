# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=unused-import

import sys
import numpy
import pygame

pygame.init()
screen = pygame.display.set_mode([500, 500])

class Memory:
    def __init__(self):
        self.buffer = bytearray([0] * 4096)
    def read(self, addr):
        return self.buffer[addr]
    def write(self, addr, value):
        self.buffer[addr] = value
    def dump(self):
        pass

class CPU:
    def __init__(self):
        self.v  = bytearray([0] * 16)
        self.i  = 0
        self.pc = 0x200
        self.sp = 0

        self.stack  = bytearray([0] * 16)
        self.timer = {
            'delay' : 0,
            'sound' : 0
        }

    def dump(self):
        print(f'v:{self.v}\n\
                \ri:{hex(self.i)}\n\
                \rpc:{hex(self.pc)}\n\
                \rsp:{hex(self.sp)}\n\
                \rstack:{self.stack}')

class Display:
    def __init__(self, surface):

        self.cols = 128
        self.rows = 128 

        self.scale = 5

        self.buffer = [ [0 for x in range(0, 128)] for y in range(0, 128) ]
        self.screen = surface
    
    def render(self):
        for row in range(0, len(self.buffer)):
            for col in range(0, len(self.buffer[row])):
                if self.buffer[row][col]:
                    pygame.draw.rect(self.screen, 0xffffff , (
                        col * self.scale, 
                        row * self.scale, 
                        self.scale, 
                        self.scale
                    ))
    def clear(self):
        self.buffer = [ [0 for x in range(0, 128)] for y in range(0, 128) ]

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

            opcode = (self.memory.read(self.cpu.pc) << 8) | self.memory.read(self.cpu.pc + 1)
            if self.dbg:
                print(f'opcode:{hex(opcode)}')
                self.cpu.dump()
                input()
            self.execute(opcode)
            
            self.video.render()
            pygame.display.flip()

    def execute(self, opcode):

        operation = (opcode & 0xf000) >> 12
        x    = (opcode & 0x0f00) >> 8
        y    = (opcode & 0x00f0) >> 4
        n    =  opcode & 0x000f
        kk   =  opcode & 0x00ff
        nnn  =  opcode & 0x0fff

        # print(f'''
        #   \ropcode   : {hex(opcode)}\n \
        #   \roperation: {hex(operation)}\n \
        #   \rx        : {hex(x)}\n \
        #   \ry        : {hex(y)}\n \
        #   \rkk       : {hex(kk)}\n \
        #   \rnnn      : {hex(nnn)}
        # ''')
        self.cpu.pc += 2 

        if   operation == 0x0: self.CLS_RET(opcode)
        elif operation == 0x1: self.JP(nnn)
        elif operation == 0x2: self.CALL(nnn)
        elif operation == 0x3: self.SE(x, kk)
        elif operation == 0x4: self.SNE(x, kk)
        elif operation == 0x5: self.SE_Vx_Vy(x, y)
        elif operation == 0x6: self.LD_VX(x, kk)
        elif operation == 0x7: self.ADD_VX(x, kk)
        elif operation == 0x8:
            logical_operation = opcode & 0xf
            if   logical_operation == 0x0: self.lo_ld(x, y)
            elif logical_operation == 0x1: self.lo_or(x, y)
            elif logical_operation == 0x2: self.lo_and(x, y)
            elif logical_operation == 0x3: self.lo_xor(x, y)
            elif logical_operation == 0x5: self.lo_sub(x, y)
            elif logical_operation == 0x7: self.lo_subn(x, y)
            elif logical_operation == 0xe: self.lo_shl(x, y)
            else: raise NotImplementedError(f'Instruction: {hex(operation)}, logical_operation:{hex(logical_operation)} not NotImplemented')

        elif operation == 0xa: self.LD_I(nnn)
        elif operation == 0xc: self.RND(x, kk)
        elif operation == 0xd: self.DRAW(x, y, n)
        elif operation == 0xe:
            sys.exit('__NOT__IMPLEMENTED__')
            # if kk == 0x9e: self.SK_IF_PRESS(x)
            # if kk == 0xa1: self.SK_NOT_PRESS(x)

        elif operation == 0xf:
            subroutine = opcode & 0xff
            if    subroutine == 0x55: self.fx55(x)
            elif  subroutine == 0x1e: self.fx1e(x)
            elif  subroutine == 0x15: self.fx15(x)
            elif  subroutine == 0x65: self.fx65(x)
            elif  subroutine == 0x29: self.fx29(x)
            elif  subroutine == 0x07: self.fx07(x)
            else: raise NotImplementedError(f'Instruction: {hex(operation)}, Subroutine:{hex(subroutine)} not NotImplemented')
        else: raise NotImplementedError(f'Instruction: {hex(operation)} not NotImplemented')

    # -- BEGIN Logical Operatios
    def lo_shl(self, x, y):
        self.cpu.v[0xf] = x >> 7
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
    def fx15(self, x):
        self.cpu.timer['delay'] = self.cpu.v[x]
        print(f'LD DT, V{x}')

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
        print(f'DRW V{x}, V{y}, {hex(nibble)}')       

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
# chip8.load("./ROMS/GREET")
# chip8.load("./ROMS/BLITZ")
# chip8.load("./ROMS/IBM")
# chip8.load("./ROMS/BC_TEST")
# chip8.load("./ROMS/KALEID")
chip8.load("./ROMS/PUZZLE")
chip8.tick()


