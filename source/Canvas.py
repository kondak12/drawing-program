import os, pygame

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
        self.__screenshot = None

    def __export_screen_shot(self) -> None:
        self.__screenshot = self.__display

        shot = pygame.Surface(main_settings.CANVAS_BORDERS)
        shot.blit(self.__display, (0, 0), (0, 0, main_settings.CANVAS_BORDERS[0], main_settings.CANVAS_BORDERS[1]))

        try:
            i = 1
            while True:
                if os.path.exists(main_settings.SAVE_SCREENSHOT_PATH + f"shot_{i}.jpg"):
                    i += 1
                    continue
                else:
                    pygame.image.save(shot, main_settings.SAVE_SCREENSHOT_PATH + f"shot_{i}.jpg")
                    break

        except pygame.error:
            os.mkdir(main_settings.SAVE_SCREENSHOT_PATH)
            self.__export_screen_shot()

    def __place_color_button(self, x_pos, y_pos, event, color) -> None:
        self.__button_example.draw_color(
            x_pos,
            y_pos,
            pygame.mouse.get_pos(),
            color,
            event,
            lambda: self.__hand.set_main_color(color)
        )

    def __place_instrument_button(self, x_pos, y_pos, img_name: str, event, new_instrument) -> None:
        self.__button_example.draw_instrument(
            x_pos,
            y_pos,
            pygame.mouse.get_pos(),
            img_name,
            event,
            lambda: self.__hand.set_main_instrument(new_instrument)
        )

    def __place_import_export_button(self, x_pos, y_pos, img_name: str, event, file_action) -> None:
        self.__button_example.draw_instrument(
            x_pos,
            y_pos,
            pygame.mouse.get_pos(),
            img_name,
            event,
            lambda: file_action()
        )

    def place_buttons_on_screen(self, event) -> None:
        pygame.draw.rect(self.__gui_region,
                         pygame.color.THECOLORS['grey'],
                         pygame.Rect((0, 0), (100, 1200))
                         )

        self.__place_instrument_button(0, 0, "fill", event, instruments_settings.FILL_TOOL)
        self.__place_instrument_button(50, 0, "brush", event, instruments_settings.BRUSH_TOOL)
        self.__place_instrument_button(0, 50,"rect", event, instruments_settings.PATTERN_TOOL_RECT)
        self.__place_instrument_button(50, 50, "circle", event, instruments_settings.PATTERN_TOOL_CIRCLE)

        self.__place_color_button(0, 100, event, colors.RED)
        self.__place_color_button(50, 100, event, colors.GREEN)
        self.__place_color_button(0, 150, event, colors.BLUE)
        self.__place_color_button(50, 150, event, colors.BLACK)
        self.__place_color_button(0, 200, event, colors.PURPLE)
        self.__place_color_button(50, 200, event, colors.YELLOW)
        self.__place_color_button(0, 250, event, colors.ORANGE)

        # self.__place_import_export_button(0, 750, "import", event, self.__import_screen_shot)
        self.__place_import_export_button(50, 750, "export", event, self.__export_screen_shot)

        self.__display.blit(self.__gui_region, (main_settings.SCREEN_SIZE[0] - 100, 0))

    def get_canvas_borders(self) -> (int, int):
        return self.__canvas_borders

    def set_canvas_borders(self, new_borders: (int, int)) -> None:
        self.__canvas_borders = new_borders