import pygame

from source import Instruments
from configs import colors


class Hand:

    def __init__(self, drawing_surface, sprite_path=None):
        self.__drawing_surface = drawing_surface
        self.__sprite_path = sprite_path
        self.__main_color = colors.BLACK
        self.__line_size = 30
        self.__main_instrument = Instruments.BrushTool(self.__drawing_surface,
                                                       self.__main_color,
                                                       pygame.mouse.get_pos(),
                                                       self.__line_size,
                                                       self.__sprite_path
                                                       )

    def update_position(self):
        self.__main_instrument.set_mouse_pos(pygame.mouse.get_pos())

    def draw(self) -> None:
        self.__main_instrument.draw()

    def get_main_color(self) -> colors.color:
        return self.__main_color

    def get_main_instrument(self) -> Instruments.Instrument:
        return self.__main_instrument

    def get_line_size(self) -> int:
        return self.__line_size

    def set_main_color(self, new_color: colors.color) -> None:
        self.__main_color = new_color

    def set_main_instrument(self, new_instrument: Instruments.Instrument) -> None:
        self.__main_instrument = new_instrument

    def set_line_size(self, new_size: int) -> None:
        self.__line_size = new_size