import os, pygame

from configs.main_settings import CANVAS_BORDERS
from configs.instruments_settings import DRAWING_RADIUS_BUTTON_DICT


class Button:

    def __init__(self, width, height, gui_region, canvas):
        self.__width = width
        self.__height = height
        self.__gui_region = gui_region
        self.__canvas = canvas
        self.__current_instrument_size = 1

    def draw_color(self, x_pos: int, y_pos: int, mouse_pos: (int, int), color, event, function) -> None:

        if (x_pos + CANVAS_BORDERS[0]) < mouse_pos[0] < (x_pos + self.__width + CANVAS_BORDERS[0]) and y_pos < mouse_pos[1] < (y_pos + self.__height):

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    function()

        pygame.draw.rect(self.__gui_region,
                         self.__canvas.get_hand().get_main_color(),
                         pygame.Rect(25, 375, 50, 25))

        pygame.draw.rect(self.__gui_region,
                         color,
                         pygame.Rect(x_pos, y_pos, self.__width, self.__height))

    def draw_instrument(self, x_pos: int, y_pos: int, mouse_pos: (int, int), img_name: str, event, function) -> None:

        if (x_pos + CANVAS_BORDERS[0]) < mouse_pos[0] < (x_pos + self.__width + CANVAS_BORDERS[0]) and y_pos < mouse_pos[1] < (y_pos + self.__height):

            icon = pygame.image.load(os.path.join(r"resources\imgs", f"{img_name + '_grey.jpg'}"))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    function()

        else:
            icon = pygame.image.load(os.path.join(r"resources\imgs", f"{img_name + '_black.jpg'}"))

        self.__gui_region.blit(icon, (x_pos, y_pos))

    def update_draw_radius(self, x_pos: int, y_pos: int, mouse_pos: (int, int), event) -> None:

        if (x_pos + CANVAS_BORDERS[0]) < mouse_pos[0] < (x_pos + self.__width + CANVAS_BORDERS[0]) and y_pos < mouse_pos[1] < (y_pos + self.__height):

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:

                    if self.__current_instrument_size == 3:
                        self.__current_instrument_size = 1
                    else:
                        self.__current_instrument_size += 1

                    self.__canvas.get_hand().set_line_size(DRAWING_RADIUS_BUTTON_DICT[self.__current_instrument_size][1])

        icon = pygame.image.load(os.path.join(r"resources\imgs", f"{DRAWING_RADIUS_BUTTON_DICT[self.__current_instrument_size][0] + '_black.jpg'}"))

        self.__gui_region.blit(icon, (x_pos, y_pos))