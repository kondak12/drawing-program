from abc import ABC, abstractmethod
import pygame


class Instrument(ABC):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        self.display = display
        self.draw_color = draw_color
        self.mouse_pos = mouse_pos
        self.draw_radius = draw_radius

    @abstractmethod
    def draw(self) -> None:
        pass


class BrushTool(Instrument):

    def __init__(self, display, draw_color, mouse_pos, draw_radius, sprite_path=None):
        super().__init__(display, draw_color, mouse_pos, draw_radius)
        self.__sprite_path = sprite_path

        if self.__sprite_path is not None:
            self.__sprite_size = pygame.image.load(self.__sprite_path).get_rect().size

    def draw(self) -> None:

        if pygame.mouse.get_pressed()[0] and self.__sprite_path is None:
            pygame.draw.circle(self.display, self.draw_color, self.mouse_pos, self.draw_radius)

        elif pygame.mouse.get_pressed()[0] and self.__sprite_path is not None:
            self.display.blit(self.__sprite_path,
                              (self.mouse_pos[0] - (self.__sprite_size[0] // 2),
                               self.mouse_pos[1] - self.__sprite_size[1] // 2)
                              )