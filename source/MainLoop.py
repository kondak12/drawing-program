import pygame
import sys

import configs.main_settings, configs.colors


class MainLoop:

    def __init__(self, display: pygame.display):
        self.__running = True
        self.__frames = configs.main_settings.FPS
        self.__display = display

    def run(self) -> None:
        while self.__running:

            pygame.time.Clock().tick(self.__frames)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif pygame.mouse.get_pressed()[0]:
                    pygame.draw.circle(self.__display, configs.colors.RED, pygame.mouse.get_pos(), 50)

            pygame.display.flip()

    def get_running(self) -> bool:
        return self.__running

    def set_running(self, new_status: bool) -> None:
        self.__running = new_status