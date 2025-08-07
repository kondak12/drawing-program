import pygame

from configs.main_settings import CANVAS_BORDERS, MAIN_COLOR_SHOW_COORDINATES, MAIN_INSTRUMENT_SHOW_COORDINATES
from configs.instruments_settings import LINE_SIZE
from configs.images import BUTTONS


class Button:

    def __init__(self, width, height, favorable_region, canvas):
        self.__width = width
        self.__height = height
        self.__favorable_region = favorable_region
        self.__canvas = canvas
        self.__current_line_size_index = 0

    def __in_box(self, x_pos: int, y_pos: int) -> None:
        return ((x_pos + CANVAS_BORDERS[0]) < self.__canvas.get_hand().get_mouse_pos()[0] < (x_pos + self.__width + CANVAS_BORDERS[0])
                and y_pos < self.__canvas.get_hand().get_mouse_pos()[1] < (y_pos + self.__height))

    def __is_press(self, event: pygame.event) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT

    def show_users_uses(self) -> None:
        pygame.draw.rect(
            self.__favorable_region,
            self.__canvas.get_hand().get_main_color(),
            pygame.Rect(MAIN_COLOR_SHOW_COORDINATES)
        )

    def color(self, x_pos: int, y_pos: int, color, event) -> None:

        if self.__in_box(x_pos, y_pos) and self.__is_press(event):
            self.__canvas.get_hand().set_main_color(color)

        pygame.draw.rect(
            self.__favorable_region,
            color,
            pygame.Rect(x_pos, y_pos, self.__width, self.__height)
        )

    def instrument(self, x_pos: int, y_pos: int, caps_img_name: str, event) -> None:

        if self.__in_box(x_pos, y_pos):
            icon = BUTTONS[f"{caps_img_name}"][1]

            if self.__is_press(event):
                    self.__canvas.get_hand().set_main_instrument(caps_img_name.lower())
        else:
            icon = BUTTONS[f"{caps_img_name}"][0]

        self.__favorable_region.blit(icon, (x_pos, y_pos))

    def line_size(self, x_pos: int, y_pos: int, event) -> None:

        if self.__in_box(x_pos, y_pos) and self.__is_press(event):

            if self.__current_line_size_index == 2:
                self.__current_line_size_index = 0
            else:
                self.__current_line_size_index += 1

            self.__canvas.get_hand().set_line_size(LINE_SIZE[self.__current_line_size_index])

        icon = BUTTONS["LINE_SIZE"][self.__current_line_size_index]
        self.__favorable_region.blit(icon, (x_pos, y_pos))

    def other_function(self, x_pos: int, y_pos: int, img_name, event, function) -> None:
        if self.__in_box(x_pos, y_pos):
            icon = BUTTONS[f"{img_name}"][1]

            if self.__is_press(event):
                    function()
        else:
            icon = BUTTONS[f"{img_name}"][0]

        self.__favorable_region.blit(icon, (x_pos, y_pos))