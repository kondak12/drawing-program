import pygame
import sys

from source.Canvas import Canvas
from source.Hand import Hand


class InputSystem:

    def __init__(self, surface: pygame.Surface):
        self.__surface = surface
        self.__gui = pygame.Surface((100, 1200))
        self.__hand = Hand(self.__surface)
        self.__canvas = Canvas(self.__surface, self.__hand, self.__gui)

    def handle_events(self) -> None:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.__canvas.place_buttons_on_screen(event)

            self.__canvas.do_action_screen_cycle(event)

        self.__hand.update_position()

        self.__hand.draw()

        self.__hand.wash_draw()

        pygame.display.flip()