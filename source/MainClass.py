import pygame

from configs import colors, main_settings, images
from source.MainLoop import MainLoop


class MainClass:

    def __init__(self):
        self.__screen = pygame.display.set_mode(size=main_settings.WINDOW_SIZE)
        self.__main_loop = MainLoop(self.__screen)
        self.__caption = "Drawing program"

        pygame.display.set_icon(images.PROGRAM_LOGO)
        pygame.display.set_caption(self.__caption)

    def run(self) -> None:
        pygame.init()

        self.__screen.fill(colors.WHITE)
        self.__main_loop.run()

    def set_screen_size(self, new_size: (int, int)) -> None:
        self.__screen = pygame.display.set_mode(size=new_size)