import pygame

from configs import colors, main_settings
from source.MainLoop import MainLoop


class MainClass:

    def __init__(self):
        self.__screen = pygame.display.set_mode(size=main_settings.SCREEN_SIZE)
        self.__main_loop = MainLoop(self.__screen)
        self.__caption = "Drawing program"

        pygame.display.set_icon(pygame.image.load("resources\imgs\drawing_program_logo.png"))
        pygame.display.set_caption(self.__caption)

    def run(self) -> None:
        pygame.init()

        self.__screen.fill(colors.WHITE)
        self.__main_loop.run()

    def set_screen_size(self, new_size: (int, int)) -> None:
        self.__screen = pygame.display.set_mode(size=new_size)