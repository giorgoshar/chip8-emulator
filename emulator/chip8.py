import sys
import os.path
import pygame
import random

from devices import *
pygame.init()

screen = pygame.display.set_mode([900, 600], pygame.HWSURFACE |pygame.DOUBLEBUF)
font   = pygame.font.SysFont("monospace", 14)

class Chip8:
    def __init__(self):

        self.memory= Memory(0x1000)
        self.cpu   = CPU()
        self.video = Display(screen)
        self.keyboard = Keyboard()

        self.fontset: list[bytes] = [
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

        self.toRender: bool = False

    def load(self, filename):
        self.reset()
        with open(filename, 'rb') as fp:
            rom = fp.read()

        # load fonts
        for i in range(0, len(self.fontset)):
            self.memory.write(i, self.fontset[i])

        # load rom to memory
        for offset, byte in enumerate(rom):
            self.memory.write(0x200 + offset, byte)

    def reset(self):
        self.cpu  = CPU()
        self.memory.clear()
        self.video.clear()
        self.keyboard.reset()

    def tick(self):
        self.cpu.opcode = (self.memory.read(self.cpu.pc) << 8) | self.memory.read(self.cpu.pc + 1)
        self.execute(self.cpu.opcode)
        if self.cpu.timer['delay'] > 0: 
            self.cpu.timer['delay'] -= 1
        if self.cpu.timer['sound'] > 0: 
            self.cpu.timer['sound'] -= 1

    def run(self):
        clock    = pygame.time.Clock()
        running  = True
        mem_scroll_y = 0x200
        while running:
            clock.tick(1000 / 60)
            screen.fill((0, 0, 0))      
            # keyboard events
            self.keyboard.handle()
            self.tick()

            # render everything to screen
            self.video.render()
            pygame.display.flip()

    def execute(self, opcode):

        ins = (opcode & 0xf000) >> 12
        x   = (opcode & 0x0f00) >> 8
        y   = (opcode & 0x00f0) >> 4
        n   =  opcode & 0x000f
        kk  =  opcode & 0x00ff
        nnn =  opcode & 0x0fff

        self.cpu.pc += 2

        # ==[ main operations ]==
        if   ins == 0x0 and (opcode & 0xff) == 0xe0: self.CLS()
        elif ins == 0x0 and (opcode & 0xff) == 0xee: self.RET()
        elif ins == 0x1: self.JP(nnn)
        elif ins == 0x2: self.CALL(nnn)
        elif ins == 0x3: self.SE_Vx_kk(x, kk)
        elif ins == 0x4: self.SNE_Vx_kk(x, kk)
        elif ins == 0x5: self.SE_Vx_Vy(x, y)
        elif ins == 0x6: self.LD_VX(x, kk)
        elif ins == 0x7: self.ADD_VX(x, kk)
        elif ins == 0x9: self.SNE_Vx_Vy(x, y)
        elif ins == 0xa: self.LD_I(nnn)
        elif ins == 0xc: self.RND(x, kk)
        elif ins == 0xd: self.DRAW(x, y, n)

        # ==[ input operations ]==
        elif ins == 0xe and (opcode & 0xff) == 0x9e: self.skp_pressed(x)
        elif ins == 0xe and (opcode & 0xff) == 0xa1: self.skp_not_pressed(x)

        # ==[ logical operations ]==
        elif ins == 0x8 and (opcode & 0xf) == 0x0: self.lo_ld(x, y)
        elif ins == 0x8 and (opcode & 0xf) == 0x1: self.lo_or(x, y)
        elif ins == 0x8 and (opcode & 0xf) == 0x2: self.lo_and(x, y)
        elif ins == 0x8 and (opcode & 0xf) == 0x3: self.lo_xor(x, y)
        elif ins == 0x8 and (opcode & 0xf) == 0x4: self.lo_add(x, y)
        elif ins == 0x8 and (opcode & 0xf) == 0x5: self.lo_sub(x, y)
        elif ins == 0x8 and (opcode & 0xf) == 0x6: self.lo_shr(x, y)
        elif ins == 0x8 and (opcode & 0xf) == 0x7: self.lo_subn(x, y)
        elif ins == 0x8 and (opcode & 0xf) == 0xe: self.lo_shl(x, y)

        # ==[ subroutine operations ]==
        elif ins == 0xf and (opcode & 0xff) == 0x07: self.fx07(x)
        elif ins == 0xf and (opcode & 0xff) == 0x0a: self.fx0a(x)
        elif ins == 0xf and (opcode & 0xff) == 0x55: self.fx55(x)
        elif ins == 0xf and (opcode & 0xff) == 0x1e: self.fx1e(x)
        elif ins == 0xf and (opcode & 0xff) == 0x15: self.fx15(x)
        elif ins == 0xf and (opcode & 0xff) == 0x18: self.fx18(x)
        elif ins == 0xf and (opcode & 0xff) == 0x65: self.fx65(x)
        elif ins == 0xf and (opcode & 0xff) == 0x29: self.fx29(x)
        elif ins == 0xf and (opcode & 0xff) == 0x33: self.fx33(x)
        
        # Super Chip-48 Instructions
        elif ins == 0xf and (opcode & 0xff) == 0x75: sys.exit('super chip8 not implemented')
        elif ins == 0xf and (opcode & 0xff) == 0x85: sys.exit('super chip8 not implemented')
        else: exit(f'Failed to execute opcode: {hex(opcode)} (addr: 0x{self.cpu.pc:x})')

    # -- BEGIN MAIN OPERATIONS
    def RND(self, x, kk):
        rnd = random.randint(0x0, 0xff)
        self.cpu.v[x] = rnd & kk
    def JP(self, nnn):
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
        self.toRender = True
            
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
    def LD_VX(self, x, kk):
        self.cpu.v[x] = kk
    def CLS(self):
        self.video.clear()
    def RET(self):
        self.cpu.pc = self.cpu.stack[ self.cpu.sp - 1 ]
        self.cpu.sp -= 1
    # -- END MAIN OPERATIONS

    # -- BEGIN INPUT HANDLE
    def skp_pressed(self, x):
        if self.keyboard.keypad[x] == 1:
            self.cpu.pc += 2
    def skp_not_pressed(self, x):
        if self.keyboard.keypad[x] == 0:
            self.cpu.pc += 2
    # -- END INPUT HANDLE

    # -- BEGIN Logical Operatios
    def lo_ld(self, x, y):
        self.cpu.v[x] = self.cpu.v[y]
    def lo_or(self, x, y):
        self.cpu.v[x] |= self.cpu.v[y]
    def lo_and(self, x, y):
        self.cpu.v[x] &= self.cpu.v[y]
    def lo_xor(self, x, y):
        self.cpu.v[x] ^= self.cpu.v[y]
    def lo_add(self, x, y):
        if (self.cpu.v[x] + self.cpu.v[y]) > 0xff:
            self.cpu.v[0xf] = 1
        else:
            self.cpu.v[0xf] = 0
        self.cpu.v[x] = (self.cpu.v[x] + self.cpu.v[y]) & 0xff
    def lo_sub(self, x, y):
        if self.cpu.v[x] >= self.cpu.v[y]:
            self.cpu.v[0xf] = 1
        else:
            self.cpu.v[0xf] = 0
        self.cpu.v[x] = (self.cpu.v[x] - self.cpu.v[y]) & 0xff
    def lo_shr(self, x, y):
        self.cpu.v[0xF] = self.cpu.v[x] & 0x1
        self.cpu.v[x] = (self.cpu.v[x] >> 1) & 0xff
    def lo_subn(self, x, y):
        if self.cpu.v[y] >= self.cpu.v[x]:
            self.cpu.v[0xf] = 1
        else:
            self.cpu.v[0xf] = 0
        self.cpu.v[x] = (self.cpu.v[y] - self.cpu.v[x]) & 0xff
    def lo_shl(self, x, y):
        self.cpu.v[0xF] = self.cpu.v[x] >> 7
        self.cpu.v[x]   = (self.cpu.v[x] << 1) & 0xff
    # -- END Logical Operations    
 
    # -- BEGIN Subroutine Operations
    def fx07(self, x):
        self.cpu.v[x] = self.cpu.timer['delay']
    def fx0a(self, x):
        # wait for key to pressed
        pressed = False
        while not pressed:
            self.keyboard.handle()
            for key in range(0, len(self.keyboard.keypad)):
                if self.keyboard.keypad[key] == 0x1:
                    self.cpu.v[x] = key
                    pressed = True   
    def fx33(self, x): # BCD
        self.memory.write(self.cpu.i + 0, self.cpu.v[x] // 100)
        self.memory.write(self.cpu.i + 1, self.cpu.v[x] % 100 // 10)
        self.memory.write(self.cpu.i + 2, self.cpu.v[x] % 10)
    def fx15(self, x):
        self.cpu.timer['delay'] = self.cpu.v[x]
    def fx18(self, x):
        self.cpu.timer['sound'] = self.cpu.v[x]
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

class Window:
    def __init__(self, width, height, x, y):
        self.surface = pygame.Surface((width, height))
        self.rect    = pygame.Rect((x, y), (width, height))
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)

class Emulator:
    def __init__(self, screen):
        self.chip8 = Chip8()
        self.isRunning = True
        
        self.screen = screen
        # maybe subsurface is better?
        self.memoryWindowView   = pygame.Surface((400, 400))
        self.registerWindowView = pygame.Surface((300, 150))
        self.keyboardWindowView = pygame.Surface((200, 150))

        self.beginMemView = self.chip8.cpu.pc - 10
        self.endMemView   = self.chip8.cpu.pc + 10

        self.state = 1 # 1 = run, 2 = debug
        self.init()

    def init(self):
        self.chip8.keyboard.keys[pygame.K_w] = 0x0
        self.chip8.keyboard.keys[pygame.K_s] = 0x1


    def run(self, romname):
        self.chip8.load(romname)
        clock = pygame.time.Clock()
        while self.isRunning:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if   event.key == pygame.K_F1: self.state = 1
                    elif event.key == pygame.K_F2: self.state = 2

                    elif event.key == pygame.K_n and self.state == 2:
                        self.chip8.tick()

                self.chip8.keyboard.fire(event)

            # switch states
            if self.state == 1:
                self.chip8.tick()

            if self.chip8.toRender == True:
                self.chip8.video.render(self.screen)
                self.chip8.toRender = False

            self.updateMemoryWindow()
            self.updateRegistersWindow()
            self.updateKeyboardWindow()

            pygame.display.flip()
    
    def bind(self, pkey, vkey):
        self.chip8.keyboard.keys[pkey] = vkey

    def updateMemoryWindow(self):
        self.memoryWindowView.fill((0, 0, 0))
        y = 0
        
        if self.chip8.cpu.pc not in range(self.beginMemView + 5, self.endMemView - 5):
            self.beginMemView = self.chip8.cpu.pc - 20
            self.endMemView   = self.chip8.cpu.pc + 20
 
        for i in range(self.beginMemView, self.endMemView, 2):
            color = (255, 0, 0) if i == self.chip8.cpu.pc else (255, 255, 255)
            text  = font.render(f"{i:>04x}: {self.chip8.memory.buffer[i]:>02x} {self.chip8.memory.buffer[i + 1]:02x}", True, color)
            self.memoryWindowView.blit(text, (0, y))
            y += 16

        self.add_border(self.memoryWindowView)
        self.screen.blit(self.memoryWindowView, (515, 0))      

    def updateRegistersWindow(self):
        self.registerWindowView.fill((0, 0, 0))
        x = 0
        y = 0
        for reg in range(0, len(self.chip8.cpu.v)):
            text = font.render(f'V{reg}:0x{self.chip8.cpu.v[reg]:x} ', True, (255, 255, 255))
            self.registerWindowView.blit(text, (y, x))
            x += 16
            if x >= (16 * 8):
                x = 0
                y += 80

        text = font.render(f'I :{hex(self.chip8.cpu.i)}', True, (255, 255, 255))
        self.registerWindowView.blit(text, (160, 0))

        text = font.render(f'PC:{hex(self.chip8.cpu.pc)}', True, (255, 255, 255))
        self.registerWindowView.blit(text, (160, 16))

        text = font.render(f'SP:{hex(self.chip8.cpu.sp)}', True, (255, 255, 255))
        self.registerWindowView.blit(text, (160, 32))
        
        self.add_border(self.registerWindowView)
        self.screen.blit(self.registerWindowView, (0, 260))

    def updateKeyboardWindow(self):
        self.keyboardWindowView.fill((0, 0, 0))
        x = 0
        y = 0
        for key in range(0, len(self.chip8.keyboard.keypad)):
            text = font.render(f'key_{key}:{self.chip8.keyboard.keypad[key]}', True, (255, 255, 255))
            self.keyboardWindowView.blit(text, (y, x))
            x += 16
            if x >= (16 * 8):
                x = 0
                y += 80
        
        self.add_border(self.keyboardWindowView)
        self.screen.blit(self.keyboardWindowView, (300, 260))
    
    def updateScreenWindow(self): pass

    def add_border(self, window, border_width = 1, color = (255, 255, 255)):
        box_width  = window.get_width()
        box_height = window.get_height()
        pygame.draw.lines(
            window, 
            color,
            False,
            [
                [0, 0],
                [box_width - 1, 0],
                [box_width - 1, box_height - 1],
                [0, box_height - 1],
                [0, 0]
            ],
            border_width
        )
# chip8 = Chip8()

# romname = "./ROMS/KALEID"
# romname = "./ROMS/PUZZLE"
# romname = "./ROMS/test_opcode.ch8"
# romname = "./ROMS/IBM"
# romname = "./ROMS/BC_TEST"
# romname = "./ROMS/MISSILE"
# romname = "./ROMS_TEST/test_opcode.ch8"

romname = "./IBM"
if len(sys.argv) == 2:
    if os.path.isfile(sys.argv[1]):
        romname = sys.argv[1]
    else:
        sys.exit(f'[__ERROR__] file {sys.argv[1]} doesnt exist')
emu = Emulator(screen)
emu.state = 1
emu.run(romname)

# chip8.load(romname)
# chip8.run()