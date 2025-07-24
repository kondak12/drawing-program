import pygame
import sys

from source.Hand import Hand


class InputSystem:

    def __init__(self, surface: pygame.Surface):
        self.__surface = surface
        self.__hand = Hand(self.__surface)

    def handle_events(self) -> None:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif pygame.mouse.get_pressed()[0]:
                self.__hand.update_position()
                self.__hand.draw()

            pygame.display.flip()