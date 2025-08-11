import pygame


class SurfaceStub:

    def __init__(self, size=(800, 600), flags=0):
        self.size = size
        self.flags = flags
        self.color = pygame.Color(0, 0, 0, 255)
        self.pixels = {}
        self.blit_called = False
        self.fill_called = False
        self.convert_called = False

    def fill(self, color):
        self.fill_called = True
        self.color = color

    def convert(self):
        self.convert_called = True
        return self

    def get_size(self):
        return self.size

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]

    def get_at(self, pos):
        return self.pixels.get(pos, self.color)

    def set_at(self, pos, color):
        self.pixels[pos] = color

    def blit(self, source, dest, area=None):
        self.blit_called = True

    def copy(self):
        new_surface = SurfaceStub(self.size, self.flags)
        new_surface.pixels = self.pixels.copy()
        return new_surface