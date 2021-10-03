import pygame

class Display:
    def __init__(self, surface):

        self.cols  = 64
        self.rows  = 32 
        self.scale = 8

        self.buffer = [ [0 for x in range(0, self.cols)] for y in range(0, self.rows) ]
        self.screen = surface

        self.toRender = False

    def render(self, screen = None):
        surface = self.screen if screen is None else screen
        for row in range(0, len(self.buffer)):
            for col in range(0, len(self.buffer[row])):
                color = 0x1e1e1e
                rect  = (col * self.scale, row * self.scale, self.scale, self.scale)
                if self.buffer[row][col] != 0:
                    color = 0xdcdc9f
                pygame.draw.rect(surface, color , rect)
    
    def clear(self):
        self.buffer = [ [0 for x in range(0, self.cols)] for y in range(0, self.rows) ]

    def __repr__(self):
        string = ''
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                char = '.'
                if self.buffer[row][col] == 1:
                    char = '#'
                string += char
            string += '\n'
        return string