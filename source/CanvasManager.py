import pygame

from configs import main_settings, colors
from configs.instruments_settings import BRUSH_TOOL, FILL_TOOL, RECT_TOOL, CIRCLE_TOOL
from source import gui, Hand
from source.FileHandler import FileHandler
from configs.main_settings import (
    APPROVED_CANVAS_ACTIONS, UNAPPROVED_CANVAS_ACTIONS,
    CANVAS_SIZE, ZERO_COORDINATES,
    CANVAS_BOX, GUI_REGION_SIZE,
    ACTION_BACK, ACTION_FORWARD,
    EXPORT, IMPORT
)


class CanvasManager:

    def __init__(self, canvas, hand: Hand, gui_region_surface):
        self.__canvas = canvas
        self.__hand = hand
        self.__gui_region_surface = gui_region_surface
        self.__file_handler = FileHandler(self.__canvas)

        self.__gui_zone = gui.GUIZone(self.__gui_region_surface, GUI_REGION_SIZE[0], GUI_REGION_SIZE[1])
        self.__color_btn = gui.ColorButton(50, 50, self.__gui_region_surface, self)
        self.__instrument_btn = gui.InstrumentButton(50, 50, self.__gui_region_surface, self)
        self.__function_btn = gui.FunctionButton(50, 50, self.__gui_region_surface, self)
        self.__line_btn = gui.LineSizeButton(50, 50, self.__gui_region_surface, self)

        self.__current_action_screen = APPROVED_CANVAS_ACTIONS
        self.__action_screen_sequence = {
            UNAPPROVED_CANVAS_ACTIONS: None,
            APPROVED_CANVAS_ACTIONS: pygame.Surface(CANVAS_SIZE)
        }
        self.__action_screen_sequence[APPROVED_CANVAS_ACTIONS].fill(main_settings.BG_COLOR)

    def __check_cycle_condition(self, event: pygame.event) -> bool:
        return event.type == pygame.MOUSEBUTTONUP and (event.button == pygame.BUTTON_LEFT or event.button == pygame.BUTTON_RIGHT)

    def do_action_screen_cycle(self, event) -> None:
        if not self.__hand.in_gui_borders() and self.__check_cycle_condition(event):

            new_surface = pygame.Surface(CANVAS_SIZE)

            new_surface.blit(
                self.__canvas,
                ZERO_COORDINATES,
                CANVAS_BOX
            )

            if self.__current_action_screen == APPROVED_CANVAS_ACTIONS:
                self.__action_screen_sequence[UNAPPROVED_CANVAS_ACTIONS] = self.__action_screen_sequence[APPROVED_CANVAS_ACTIONS]
            else:
                self.__current_action_screen = APPROVED_CANVAS_ACTIONS

            self.__action_screen_sequence[APPROVED_CANVAS_ACTIONS] = new_surface

    def __back_action(self) -> None:
        if self.__action_screen_sequence[UNAPPROVED_CANVAS_ACTIONS] is not None:
            self.__current_action_screen = UNAPPROVED_CANVAS_ACTIONS
            self.__canvas.blit(
                self.__action_screen_sequence[UNAPPROVED_CANVAS_ACTIONS],
                ZERO_COORDINATES,
                CANVAS_BOX
            )

    def __forward_action(self) -> None:
        self.__current_action_screen = APPROVED_CANVAS_ACTIONS
        self.__canvas.blit(
            self.__action_screen_sequence[APPROVED_CANVAS_ACTIONS],
            ZERO_COORDINATES,
            CANVAS_BOX
        )

    def place_gui_on_screen(self, event) -> None:
        self.__gui_zone.place(ZERO_COORDINATES)

        self.__instrument_btn.place(0, 0, event, FILL_TOOL)
        self.__instrument_btn.place(50, 0, event, BRUSH_TOOL)
        self.__instrument_btn.place(0, 50, event, RECT_TOOL)
        self.__instrument_btn.place(50, 50, event, CIRCLE_TOOL)

        self.__color_btn.place(0, 100, event, colors.RED)
        self.__color_btn.place(50, 100, event, colors.GREEN)
        self.__color_btn.place(0, 150, event, colors.BLUE)
        self.__color_btn.place(50, 150, event, colors.BLACK)
        self.__color_btn.place(0, 200, event, colors.PURPLE)
        self.__color_btn.place(50, 200, event, colors.YELLOW)
        self.__color_btn.place(0, 250, event, colors.ORANGE)
        self.__color_btn.place(50, 250, event, colors.BLUE_GREEN)
        self.__color_btn.place(0, 300, event, colors.MAROON)
        self.__color_btn.place(50, 300, event, colors.CYAN)
        self.__color_btn.place(0, 350, event, colors.PINK)
        self.__color_btn.place(50, 350, event, colors.ORCHID)

        self.__color_btn.place_current_color()
        self.__instrument_btn.place_current_instrument()
        self.__line_btn.place(25, 550, event)

        self.__function_btn.place(50, 650, event, ACTION_FORWARD, self.__forward_action)
        self.__function_btn.place(0, 650, event, ACTION_BACK, self.__back_action)

        self.__function_btn.place(0, 750, event, IMPORT, self.__file_handler.import_file)
        self.__function_btn.place(50, 750, event, EXPORT, self.__file_handler.export_file)

        self.__canvas.blit(self.__gui_region_surface, main_settings.GUI_REGION_POSITION)

    def get_hand(self) -> Hand:
        return self.__hand