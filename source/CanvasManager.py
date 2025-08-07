import pygame, tkinter

from tkinter import filedialog
from configs import main_settings, colors, paths
from configs.main_settings import APPROVED_CANVAS_ACTIONS, UNAPPROVED_CANVAS_ACTIONS, CANVAS_BORDERS, ZERO_COORDINATES
from source import gui, Hand


class CanvasManager:

    def __init__(self, display, hand: Hand, gui_box):
        self.__display = display
        self.__hand = hand
        self.__gui_box = gui_box
        self.__button_example = gui.Button(50, 50, self.__gui_box, self)
        self.__screenshot_box = main_settings.SCREENSHOT_BOX
        self.__screenshot = None

        self.__current_action_screen = APPROVED_CANVAS_ACTIONS
        self.__action_screen_sequence = {
            UNAPPROVED_CANVAS_ACTIONS: None,
            APPROVED_CANVAS_ACTIONS: pygame.Surface(CANVAS_BORDERS)
        }
        self.__action_screen_sequence[APPROVED_CANVAS_ACTIONS].fill(main_settings.BG_COLOR)

    def __check_cycle_condition(self, event: pygame.event) -> bool:
        return event.type == pygame.MOUSEBUTTONUP and (event.button == pygame.BUTTON_LEFT or event.button == pygame.BUTTON_RIGHT)

    def do_action_screen_cycle(self, event) -> None:
        if not self.__hand.in_display_borders() and self.__check_cycle_condition(event):

            new_surface = pygame.Surface(CANVAS_BORDERS)

            new_surface.blit(
                self.__display,
                ZERO_COORDINATES,
                (0, 0, CANVAS_BORDERS[0], CANVAS_BORDERS[1])
            )

            if self.__current_action_screen == APPROVED_CANVAS_ACTIONS:
                self.__action_screen_sequence[APPROVED_CANVAS_ACTIONS], self.__action_screen_sequence[UNAPPROVED_CANVAS_ACTIONS] \
                    = new_surface, self.__action_screen_sequence[APPROVED_CANVAS_ACTIONS]

            else:
                self.__action_screen_sequence[APPROVED_CANVAS_ACTIONS] = new_surface
                self.__current_action_screen = APPROVED_CANVAS_ACTIONS

    def __back_action(self) -> None:
        if self.__action_screen_sequence[UNAPPROVED_CANVAS_ACTIONS] is not None:
            self.__current_action_screen = UNAPPROVED_CANVAS_ACTIONS
            self.__display.blit(
                self.__action_screen_sequence[UNAPPROVED_CANVAS_ACTIONS],
                ZERO_COORDINATES,
                (0, 0, CANVAS_BORDERS[0], CANVAS_BORDERS[1])
            )

    def __forward_action(self) -> None:
        self.__current_action_screen = APPROVED_CANVAS_ACTIONS
        self.__display.blit(
            self.__action_screen_sequence[APPROVED_CANVAS_ACTIONS],
            ZERO_COORDINATES,
            (0, 0, CANVAS_BORDERS[0], CANVAS_BORDERS[1])
        )

    def __check_import_img_size(self, img: pygame.Surface) -> bool:
        return ((img.get_width() != CANVAS_BORDERS[0] or img.get_height() != CANVAS_BORDERS[1])
                and img.get_width() < CANVAS_BORDERS[0])

    def __import_screen_shot(self) -> None:
        main_settings.IMPORT_SCREENSHOT_PATH = tkinter.filedialog.askopenfile()

        if paths.IMPORT_SCREENSHOT is not None:

            try:
                new_surface = pygame.image.load(paths.IMPORT_SCREENSHOT).convert()
            except pygame.error:
                return

            if self.__check_import_img_size(new_surface):
                x_pos = (CANVAS_BORDERS[0] // 2) - (new_surface.get_width() // 2)
            else:
                x_pos = 0

            self.__display.blit(
                new_surface,
                (x_pos, 0),
                (0, 0, CANVAS_BORDERS[0], CANVAS_BORDERS[1])
            )

    def __export_screen_shot(self) -> None:
        self.__screenshot = self.__display

        shot = pygame.Surface(CANVAS_BORDERS)
        shot.blit(
            self.__display,
            ZERO_COORDINATES,
            (0, 0, CANVAS_BORDERS[0], CANVAS_BORDERS[1])
        )

        main_settings.EXPORT_SCREENSHOT_PATH = tkinter.filedialog.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension="png",
            initialfile="saved_picture"
        )

        try:
            if paths.EXPORT_SCREENSHOT[:4] == ".png":
                pygame.image.save(shot, paths.EXPORT_SCREENSHOT[:-4])
            else:
                pygame.image.save(shot, paths.EXPORT_SCREENSHOT)

        except pygame.error:
            return

    def __place_color_button(self, x_pos, y_pos, event, color) -> None:
        self.__button_example.color(x_pos, y_pos, color, event)

    def __place_instrument_button(self, x_pos, y_pos, img_name: str, event) -> None:
        self.__button_example.instrument(x_pos, y_pos, img_name, event)

    def __place_function_button(self, x_pos, y_pos, img_name: str, event, function) -> None:
        self.__button_example.other_function(x_pos, y_pos, img_name, event, function)

    def __place_draw_size_button(self, x_pos, y_pos, event) -> None:
        self.__button_example.line_size(x_pos, y_pos, event)

    def __place_gui_bottom(self, place_coord: tuple, box_size: tuple) -> None:
        pygame.draw.rect(
            self.__gui_box,
            pygame.color.THECOLORS['grey'],
            pygame.Rect(place_coord, box_size)
        )

    def place_gui_on_screen(self, event) -> None:
        self.__place_gui_bottom(ZERO_COORDINATES, main_settings.GUI_BOX_SIZE)

        self.__place_instrument_button(0, 0, "FILL", event)
        self.__place_instrument_button(50, 0, "BRUSH", event)
        self.__place_instrument_button(0, 50,"RECT", event)
        self.__place_instrument_button(50, 50, "CIRCLE", event)

        self.__place_color_button(0, 100, event, colors.RED)
        self.__place_color_button(50, 100, event, colors.GREEN)
        self.__place_color_button(0, 150, event, colors.BLUE)
        self.__place_color_button(50, 150, event, colors.BLACK)
        self.__place_color_button(0, 200, event, colors.PURPLE)
        self.__place_color_button(50, 200, event, colors.YELLOW)
        self.__place_color_button(0, 250, event, colors.ORANGE)

        self.__button_example.show_users_uses()
        self.__place_draw_size_button(25, 400, event)

        self.__place_function_button(50, 650, "ACTION_FORWARD", event, self.__forward_action)
        self.__place_function_button(0, 650, "ACTION_BACK", event, self.__back_action)

        self.__place_function_button(0, 750, "IMPORT", event, self.__import_screen_shot)
        self.__place_function_button(50, 750, "EXPORT", event, self.__export_screen_shot)

        self.__display.blit(self.__gui_box, main_settings.GUI_BOX_POSITION)

    def get_hand(self) -> Hand:
        return self.__hand
