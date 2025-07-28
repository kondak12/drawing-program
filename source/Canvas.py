import pygame

import configs.main_settings


class Canvas:

    def __init__(self):
        self.__canvas_borders = configs.main_settings.CANVAS_BORDERS
        self.__screenshot_box = configs.main_settings.SCREENSHOT_BOX
        self.__example = ...

    def __screenshot(self, canvas, path: configs.main_settings.SAVE_SCREENSHOT_PATH) -> None:
        ...

    def get_canvas_borders(self) -> (int, int):
        return self.__canvas_borders

    def set_canvas_borders(self, new_borders: (int, int)) -> None:
        self.__canvas_borders = new_borders