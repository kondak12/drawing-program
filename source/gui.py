import pygame

from abc import ABC, abstractmethod

from configs.main_settings import CANVAS_SIZE, MAIN_COLOR_SHOW_COORDINATES, MAIN_INSTRUMENT_SHOW_COORDINATES
from configs.instruments_settings import LINE_SIZE
from configs.images import BUTTONS


class GUIZone:

    def __init__(self, canvas, width, height):
        self.__canvas = canvas
        self.__width = width
        self.__height = height
        self.__box_size = (width, height)

    def place(self, place_coord: tuple) -> None:
        pygame.draw.rect(
            self.__canvas,
            pygame.color.THECOLORS['grey'],
            pygame.Rect(place_coord, self.__box_size)
        )


class AbstractButton(ABC):
    def __init__(self, width, height, favorable_region_surface, canvas_manager):
        self._width = width
        self._height = height
        self._favorable_region_surface = favorable_region_surface
        self._canvas_manager = canvas_manager

    def _in_box(self, x_pos: int, y_pos: int) -> bool:
        mouse_x, mouse_y = self._canvas_manager.get_hand().get_mouse_pos()
        left_gui_border = x_pos + CANVAS_SIZE[0]
        right_gui_border = x_pos + self._width + CANVAS_SIZE[0]
        upper_gui_border = y_pos
        lower_gui_border = y_pos + self._height

        return left_gui_border < mouse_x < right_gui_border and upper_gui_border < mouse_y < lower_gui_border

    def _is_press(self, event: pygame.event) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT

    @abstractmethod
    def place(self, x_pos: int, y_pos: int, event, **kwargs) -> None:
        pass


class ColorButton(AbstractButton):
    def __init__(self, width, height, favorable_region_surface, canvas_manager):
        super().__init__(width, height, favorable_region_surface, canvas_manager)

    def place_current_color(self) -> None:
        pygame.draw.rect(
            self._favorable_region_surface,
            self._canvas_manager.get_hand().get_main_color(),
            pygame.Rect(MAIN_COLOR_SHOW_COORDINATES)
        )

    def place(self, x_pos: int, y_pos: int, event, color=None) -> None:
        if self._in_box(x_pos, y_pos) and self._is_press(event):
            self._canvas_manager.get_hand().set_main_color(color)

        pygame.draw.rect(
            self._favorable_region_surface,
            color,
            pygame.Rect(x_pos, y_pos, self._width, self._height)
        )


class InstrumentButton(AbstractButton):

    def __init__(self, width, height, favorable_region_surface, canvas_manager):
        super().__init__(width, height, favorable_region_surface, canvas_manager)

    def place_current_instrument(self) -> None:
        current_instrument = self._canvas_manager.get_hand().get_main_instrument_type()

        self._favorable_region_surface.blit(
            BUTTONS[current_instrument][0],
            MAIN_INSTRUMENT_SHOW_COORDINATES
        )

    def place(self, x_pos: int, y_pos: int, event, caps_img_name=None, **kwargs) -> None:
        if self._in_box(x_pos, y_pos):
            icon = BUTTONS[f"{caps_img_name}"][1]

            if self._is_press(event):
                self._canvas_manager.get_hand().set_main_instrument(caps_img_name)

        else:
            icon = BUTTONS[f"{caps_img_name}"][0]

        self._favorable_region_surface.blit(icon, (x_pos, y_pos))


class LineSizeButton(AbstractButton):

    def __init__(self, width, height, favorable_region_surface, canvas_manager):
        super().__init__(width, height, favorable_region_surface, canvas_manager)
        self._current_line_size_index = 0

    def place(self, x_pos: int, y_pos: int, event, **kwargs) -> None:
        if self._in_box(x_pos, y_pos) and self._is_press(event):
            self._current_line_size_index = (self._current_line_size_index + 1) % 3
            self._canvas_manager.get_hand().set_line_size(LINE_SIZE[self._current_line_size_index])

        icon = BUTTONS["LINE_SIZE"][self._current_line_size_index]
        self._favorable_region_surface.blit(icon, (x_pos, y_pos))


class FunctionButton(AbstractButton):

    def __init__(self, width, height, favorable_region_surface, canvas_manager):
        super().__init__(width, height, favorable_region_surface, canvas_manager)

    def place(self, x_pos: int, y_pos: int, event, img_name=None, function=None, **kwargs) -> None:

        if self._in_box(x_pos, y_pos):
            icon = BUTTONS[f"{img_name}"][1]

            if self._is_press(event):
                function()

        else:
            icon = BUTTONS[f"{img_name}"][0]

        self._favorable_region_surface.blit(icon, (x_pos, y_pos))