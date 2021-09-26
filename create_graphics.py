import sys
import os.path
import pygame
import random

# os.environ['SDL_VIDEODRIVER'] = 'windib'
pygame.init()
screen = pygame.display.set_mode([900, 600], pygame.HWSURFACE |pygame.DOUBLEBUF)
font   = pygame.font.SysFont("monospace", 14)
clock  = pygame.time.Clock()

class Box:
    def __init__(self):
        self.surface = pygame.Surface((50, 50))
        self.rect    = self.surface.get_rect()

        self.surface.fill((255, 0, 0))    

    def render(self, surface):

        

        surface.blit(self.surface, self.rect)


b1 = Box()
isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_F1: pass
            elif event.key == pygame.K_F2: pass
    
    b1.render(screen)
    pygame.display.flip()
    
