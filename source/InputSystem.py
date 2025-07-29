import pygame
import sys

from source.Canvas import Canvas
from source.Hand import Hand
from configs import main_settings, instruments_settings, colors


class InputSystem:

    def __init__(self, surface: pygame.Surface):
        self.__surface = surface
        self.__hand = Hand(self.__surface)
        self.__canvas = Canvas(self.__surface, self.__hand)

    def handle_events(self) -> None:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.__canvas.place_color_button(
            main_settings.SCREEN_SIZE[0] - 50,
            0,
            colors.RED
        )

        self.__canvas.place_color_button(
            main_settings.SCREEN_SIZE[0] - 100,
            0, colors.BLACK
        )

        self.__canvas.place_instrument_button(
            main_settings.SCREEN_SIZE[0] - 50,
            50,
            "rect_black.jpg",
            instruments_settings.PATTERN_TOOL_RECT
        )

        self.__canvas.place_instrument_button(
            main_settings.SCREEN_SIZE[0] - 100,
            50,
            "brush_black.jpg",
            instruments_settings.BRUSH_TOOL
        )

        self.__hand.update_position()

        self.__hand.draw()

        self.__hand.wash_draw()

        pygame.display.flip()