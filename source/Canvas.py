import pygame, tkinter

from tkinter import filedialog
from configs import main_settings, colors, instruments_settings
from configs.main_settings import CANVAS_CURRENT_SCREEN_NEXT, CANVAS_CURRENT_SCREEN_PREVIOUS
from source import gui, Hand


class Canvas:

    def __init__(self, display, hand: Hand, gui_region):
        self.__display = display
        self.__hand = hand
        self.__gui_region = gui_region
        self.__button_example = gui.Button(50, 50, self.__gui_region)
        self.__canvas_borders = main_settings.CANVAS_BORDERS
        self.__screenshot_box = main_settings.SCREENSHOT_BOX
        self.__screenshot = None

        self.__current_action_screen = CANVAS_CURRENT_SCREEN_NEXT
        self.__action_screen_sequence = {
            CANVAS_CURRENT_SCREEN_PREVIOUS: None,
            CANVAS_CURRENT_SCREEN_NEXT: pygame.Surface(self.__canvas_borders)
        }
        self.__action_screen_sequence[CANVAS_CURRENT_SCREEN_NEXT].fill(main_settings.BG_COLOR)

    def do_action_screen_cycle(self, event) -> None:
        if not self.__hand.in_display_borders():

            if event.type == pygame.MOUSEBUTTONUP and (event.button == pygame.BUTTON_LEFT or event.button == pygame.BUTTON_RIGHT):
                new_surface = pygame.Surface(self.__canvas_borders)

                new_surface.blit(
                    self.__display,
                    (0, 0),
                    (0, 0, main_settings.CANVAS_BORDERS[0], main_settings.CANVAS_BORDERS[1])
                )

                if self.__current_action_screen == CANVAS_CURRENT_SCREEN_NEXT:
                    self.__action_screen_sequence[CANVAS_CURRENT_SCREEN_NEXT], self.__action_screen_sequence[CANVAS_CURRENT_SCREEN_PREVIOUS] \
                        = new_surface, self.__action_screen_sequence[CANVAS_CURRENT_SCREEN_NEXT]

                else:
                    self.__action_screen_sequence[CANVAS_CURRENT_SCREEN_NEXT] = new_surface
                    self.__current_action_screen = CANVAS_CURRENT_SCREEN_NEXT

    def __back_action(self) -> None:
        if self.__action_screen_sequence[CANVAS_CURRENT_SCREEN_PREVIOUS] is not None:
            self.__current_action_screen = CANVAS_CURRENT_SCREEN_PREVIOUS
            self.__display.blit(
                self.__action_screen_sequence[CANVAS_CURRENT_SCREEN_PREVIOUS],
                (0, 0),
                (0, 0, main_settings.CANVAS_BORDERS[0], main_settings.CANVAS_BORDERS[1])
            )

    def __forward_action(self) -> None:
        self.__current_action_screen = CANVAS_CURRENT_SCREEN_NEXT
        self.__display.blit(
            self.__action_screen_sequence[CANVAS_CURRENT_SCREEN_NEXT],
            (0, 0),
            (0, 0, main_settings.CANVAS_BORDERS[0], main_settings.CANVAS_BORDERS[1])
        )

    def __import_screen_shot(self) -> None:
        main_settings.IMPORT_SCREENSHOT_PATH = tkinter.filedialog.askopenfile()

        if main_settings.IMPORT_SCREENSHOT_PATH is not None:
            new_surface = pygame.image.load(main_settings.IMPORT_SCREENSHOT_PATH).convert()

            if ((new_surface.get_width() != self.__canvas_borders[0] or new_surface.get_height() != self.__canvas_borders[1]) and
                new_surface.get_width() < self.__canvas_borders[0]):
                self.__display.blit(
                    new_surface,
                    ((self.__canvas_borders[0] // 2) - (new_surface.get_width() // 2), 0),
                    (0, 0, main_settings.CANVAS_BORDERS[0], main_settings.CANVAS_BORDERS[1])
                )
            else:
                self.__display.blit(
                    new_surface,
                    (0, 0),
                    (0, 0, main_settings.CANVAS_BORDERS[0], main_settings.CANVAS_BORDERS[1])
                )

    def __export_screen_shot(self) -> None:
        self.__screenshot = self.__display

        shot = pygame.Surface(main_settings.CANVAS_BORDERS)
        shot.blit(
            self.__display,
            (0, 0),
            (0, 0, main_settings.CANVAS_BORDERS[0], main_settings.CANVAS_BORDERS[1])
        )

        main_settings.EXPORT_SCREENSHOT_PATH = tkinter.filedialog.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension="png",
            initialfile="saved_picture"
        )

        try:
            if main_settings.EXPORT_SCREENSHOT_PATH[:4] == ".png":
                pygame.image.save(shot, main_settings.EXPORT_SCREENSHOT_PATH[:-4])
            else:
                pygame.image.save(shot, main_settings.EXPORT_SCREENSHOT_PATH)

        except pygame.error:
            return

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

    def __place_function_button(self, x_pos, y_pos, img_name: str, event, function) -> None:
        self.__button_example.draw_instrument(
            x_pos,
            y_pos,
            pygame.mouse.get_pos(),
            img_name,
            event,
            lambda: function()
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

        self.__place_function_button(50, 600, "action_forward", event, self.__forward_action)
        self.__place_function_button(0, 600, "action_back", event, self.__back_action)

        self.__place_function_button(0, 750, "import", event, self.__import_screen_shot)
        self.__place_function_button(50, 750, "export", event, self.__export_screen_shot)

        self.__display.blit(self.__gui_region, (main_settings.SCREEN_SIZE[0] - 100, 0))

    def get_canvas_borders(self) -> (int, int):
        return self.__canvas_borders

    def set_canvas_borders(self, new_borders: (int, int)) -> None:
        self.__canvas_borders = new_borders