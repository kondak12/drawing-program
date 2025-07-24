import pygame

import configs.colors
from configs.main_settings import SCREEN_SIZE
from source.MainLoop import MainLoop


class MainClass:

    def __init__(self):
        self.__screen = pygame.display.set_mode(size=SCREEN_SIZE)
        self.__main_loop = MainLoop(self.__screen)

    def run(self) -> None:
        pygame.init()

        self.__screen.fill(configs.colors.WHITE)
        self.__main_loop.run()

    def set_screen_size(self, new_size: (int, int)) -> None:
        self.__screen = pygame.display.set_mode(size=new_size)