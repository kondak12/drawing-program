import pygame

from configs import main_settings
from source import gui, Hand


class Canvas:

    def __init__(self, display, hand: Hand):
        self.__hand = hand
        self.__display = display
        self.__canvas_borders = main_settings.CANVAS_BORDERS
        self.__screenshot_box = main_settings.SCREENSHOT_BOX
        self.__button_example = gui.Button(50, 50, self.__display)

    def place_color_button(self, x_pos, y_pos, color) -> None:
        self.__button_example.draw_color(
            x_pos,
            y_pos,
            pygame.mouse.get_pos(),
            color,
            lambda: self.__hand.set_main_color(color)
        )

    def place_instrument_button(self, x_pos, y_pos, img_name: str, new_instrument) -> None:
        self.__button_example.draw_instrument(
            x_pos,
            y_pos,
            pygame.mouse.get_pos(),
            img_name,
            lambda: self.__hand.set_main_instrument(new_instrument)
        )

    def __screenshot(self, canvas, path: main_settings.SAVE_SCREENSHOT_PATH) -> None:
        ...

    def get_canvas_borders(self) -> (int, int):
        return self.__canvas_borders

    def set_canvas_borders(self, new_borders: (int, int)) -> None:
        self.__canvas_borders = new_borders