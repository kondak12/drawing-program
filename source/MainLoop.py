import pygame
import sys


class MainLoop:

    def __init__(self):
        self.__running = True
        self.__frames = ...

    def run(self) -> None:
        while self.__running:

            pygame.time.Clock().tick(self.__frames)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def get_running(self) -> bool:
        return self.__running

    def set_running(self, new_status: bool) -> None:
        self.__running = new_status