import pygame

from configs import main_settings, colors, instruments_settings
from source import gui, Hand


class Canvas:

    def __init__(self, display, gui_region, hand: Hand):
        self.__hand = hand
        self.__gui_region = gui_region
        self.__display = display
        self.__canvas_borders = main_settings.CANVAS_BORDERS
        self.__screenshot_box = main_settings.SCREENSHOT_BOX
        self.__button_example = gui.Button(50, 50, self.__gui_region)

    def __place_color_button(self, x_pos, y_pos, color) -> None:
        self.__button_example.draw_color(
            x_pos,
            y_pos,
            pygame.mouse.get_pos(),
            color,
            lambda: self.__hand.set_main_color(color)
        )

    def __place_instrument_button(self, x_pos, y_pos, img_name: str, new_instrument) -> None:
        self.__button_example.draw_instrument(
            x_pos,
            y_pos,
            pygame.mouse.get_pos(),
            img_name,
            lambda: self.__hand.set_main_instrument(new_instrument)
        )

    def place_buttons_on_screen(self) -> None:
        pygame.draw.rect(self.__gui_region,
                         pygame.color.THECOLORS['grey'],
                         pygame.Rect((0, 0), (100, 1200))
                         )

        self.__place_instrument_button(0, 0, "brush", instruments_settings.BRUSH_TOOL)
        self.__place_instrument_button(50, 0,"rect", instruments_settings.PATTERN_TOOL_RECT)
        self.__place_instrument_button(0, 50, "fill", instruments_settings.FILL_TOOL)

        self.__place_color_button(0, 100, colors.RED)
        self.__place_color_button(50, 100, colors.GREEN)
        self.__place_color_button(0, 150, colors.BLUE)
        self.__place_color_button(50, 150, colors.BLACK)
        self.__place_color_button(0, 200, colors.PURPLE)
        self.__place_color_button(50, 200, colors.YELLOW)
        self.__place_color_button(0, 250, colors.ORANGE)

        self.__display.blit(self.__gui_region, (main_settings.SCREEN_SIZE[0] - 100, 0))

    def __screenshot(self, canvas, path: main_settings.SAVE_SCREENSHOT_PATH) -> None:
        ...

    def get_canvas_borders(self) -> (int, int):
        return self.__canvas_borders

    def set_canvas_borders(self, new_borders: (int, int)) -> None:
        self.__canvas_borders = new_borders