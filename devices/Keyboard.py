import pygame
import sys

class Keyboard:
    def __init__(self):
        self.bindKeys = {
            pygame.K_0: 0x0,
            pygame.K_1: 0x1,
            pygame.K_2: 0x2,
            pygame.K_3: 0x3,
            pygame.K_4: 0x4,
            pygame.K_5: 0x5,
            pygame.K_6: 0x6,
            pygame.K_7: 0x7,
            pygame.K_8: 0x8,
            pygame.K_9: 0x9,
            pygame.K_a: 0xa,
            pygame.K_b: 0xb,
            pygame.K_c: 0xc,
            pygame.K_d: 0xd,
            pygame.K_e: 0xe,
            pygame.K_f: 0xf,
        }
        self.keypad = [0] * len(self.bindKeys)

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key in self.bindKeys:
                    self.keypad[ self.bindKeys[event.key] ] = 0x1
            
            elif event.type == pygame.KEYUP:
                if event.key in self.bindKeys:
                    self.keypad[ self.bindKeys[event.key] ] = 0x0

    def reset(self):
        self.keypad = [0] * len(self.bindKeys)

    def isKeyPressed(self, key):
        return self.keypad[key] == 1
