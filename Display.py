import pygame

class Display:
    def __init__(self, surface):

        self.cols = 64
        self.rows = 32 

        self.scale = 5

        self.buffer = [ [0 for x in range(0, self.cols)] for y in range(0, self.rows) ]
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
        self.buffer = [ [0 for x in range(0, self.cols)] for y in range(0, self.rows) ]
