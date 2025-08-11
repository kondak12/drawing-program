import sys
import os
import pygame
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class SurfaceStub:

    def __init__(self, size=(800, 600), flags=0):
        self.size = size
        self.flags = flags
        self.color = pygame.Color(0, 0, 0, 255)
        self.pixels = {}
        self.blit_called = False
        self.fill_called = False

    def fill(self, color):
        self.fill_called = True
        self.color = color

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


@pytest.fixture(autouse=True)
def mock_pygame():
    original_init = pygame.init
    original_quit = pygame.quit
    original_set_mode = pygame.display.set_mode
    original_set_caption = pygame.display.set_caption
    original_set_icon = pygame.display.set_icon
    original_flip = pygame.display.flip
    original_get_pos = pygame.mouse.get_pos
    original_get_pressed = pygame.mouse.get_pressed
    original_event_get = pygame.event.get
    original_surface = pygame.Surface
    original_draw_rect = pygame.draw.rect
    original_draw_circle = pygame.draw.circle
    original_draw_ellipse = pygame.draw.ellipse
    original_image_load = pygame.image.load
    original_image_save = pygame.image.save

    pygame.init = lambda: None
    pygame.quit = lambda: None
    pygame.display.set_mode = lambda size, flags=0: SurfaceStub(size, flags)
    pygame.display.set_caption = lambda caption: None
    pygame.display.set_icon = lambda icon: None
    pygame.display.flip = lambda: None
    pygame.mouse.get_pos = lambda: (0, 0)
    pygame.mouse.get_pressed = lambda: (False, False, False)
    pygame.event.get = lambda: []
    pygame.Surface = SurfaceStub
    pygame.draw.rect = lambda surface, color, rect, width=0: None
    pygame.draw.circle = lambda surface, color, pos, radius: None
    pygame.draw.ellipse = lambda surface, color, rect: None
    pygame.image.load = lambda path: SurfaceStub((100, 100))
    pygame.image.save = lambda surface, path: None

    pygame.SRCALPHA = 0
    pygame.QUIT = 0
    pygame.MOUSEBUTTONDOWN = 1
    pygame.MOUSEBUTTONUP = 2
    pygame.BUTTON_LEFT = 1

    yield

    pygame.init = original_init
    pygame.quit = original_quit
    pygame.display.set_mode = original_set_mode
    pygame.display.set_caption = original_set_caption
    pygame.display.set_icon = original_set_icon
    pygame.display.flip = original_flip
    pygame.mouse.get_pos = original_get_pos
    pygame.mouse.get_pressed = original_get_pressed
    pygame.event.get = original_event_get
    pygame.Surface = original_surface
    pygame.draw.rect = original_draw_rect
    pygame.draw.circle = original_draw_circle
    pygame.draw.ellipse = original_draw_ellipse
    pygame.image.load = original_image_load
    pygame.image.save = original_image_save


@pytest.fixture
def surface_stub():
    return SurfaceStub()


@pytest.fixture
def hand_stub(surface_stub):
    from source.Hand import Hand
    hand = Hand(surface_stub)

    class BrushStub:

        def __init__(self, surface, color, pos, size):
            self.surface = surface
            self.draw_color = color
            self.mouse_pos = pos
            self.draw_radius = size
            self.draw_called = False
            self.wash_draw_called = False

        def set_mouse_pos(self, pos):
            self.mouse_pos = pos

        def set_draw_color(self, color):
            self.draw_color = color

        def set_draw_radius(self, radius):
            self.draw_radius = radius

        def draw(self):
            self.draw_called = True

        def wash_draw(self):
            self.wash_draw_called = True

    hand._Hand__main_instrument = BrushStub(surface_stub, pygame.Color('black'), (0, 0), 5)
    hand._Hand__eraser = BrushStub(surface_stub, pygame.Color('white'), (0, 0), 5)

    return hand