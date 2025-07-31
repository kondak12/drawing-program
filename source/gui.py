import os, pygame

from configs.main_settings import CANVAS_BORDERS


class Button:

    def __init__(self, width, height, display):
        self.__width = width
        self.__height = height
        self.__display = display

    def draw_color(self, x_pos: int, y_pos: int, mouse_pos: (int, int), color, function) -> None:

        if (x_pos + CANVAS_BORDERS[0]) < mouse_pos[0] < (x_pos + self.__width + CANVAS_BORDERS[0]) and y_pos < mouse_pos[1] < (y_pos + self.__height):

            if pygame.mouse.get_pressed()[0]:
                function()

        pygame.draw.rect(self.__display,
                         color,
                         pygame.Rect(x_pos, y_pos, self.__width, self.__height))

    def draw_instrument(self, x_pos: int, y_pos: int, mouse_pos: (int, int), img_name: str, function) -> None:

        if (x_pos + CANVAS_BORDERS[0]) < mouse_pos[0] < (x_pos + self.__width + CANVAS_BORDERS[0]) and y_pos < mouse_pos[1] < (y_pos + self.__height):

            icon = pygame.image.load(os.path.join(r"resources\imgs", f"{img_name + '_grey.jpg'}"))

            if pygame.mouse.get_pressed()[0]:
                function()

        else:
            icon = pygame.image.load(os.path.join(r"resources\imgs", f"{img_name + '_black.jpg'}"))

        self.__display.blit(icon, (x_pos, y_pos))