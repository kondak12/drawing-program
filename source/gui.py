import pygame


class Button:

    def __init__(self, width, height, display, color=None, picture=None):
        self.__width = width
        self.__height = height
        self.__display = display
        self.__color = color
        self.__picture = picture

    def draw(self, x_pos: int, y_pos: int, mouse_pos: (int, int), function) -> None:

        if x_pos < mouse_pos[0] < x_pos + self.__width and y_pos < mouse_pos[1] < y_pos + self.__height:

            if pygame.mouse.get_pressed()[0]:
                function()

        else:
            pygame.draw.rect(self.__display,
                             self.__color,
                             pygame.Rect(x_pos, y_pos, self.__width, self.__height))