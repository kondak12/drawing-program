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

    @abstractmethod
    def set_draw_color(self, new_color: pygame.color.Color) -> None:
        pass

    @abstractmethod
    def set_mouse_pos(self, new_pos: (int, int)) -> None:
        pass

    @abstractmethod
    def set_draw_radius(self, new_radius: int) -> None:
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

    def set_draw_color(self, new_color: pygame.color.Color) -> None:
        self.draw_color = new_color

    def set_mouse_pos(self, new_pos: (int, int)) -> None:
        self.mouse_pos = new_pos

    def set_draw_radius(self, new_radius: int) -> None:
        self.draw_radius = new_radius

    def set_sprite_path(self, new_path: str) -> None:
        self.__sprite_path = new_path