from abc import ABC, abstractmethod
import pygame

from configs import instruments_settings


class Instrument(ABC):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        self.display = display
        self.draw_color = draw_color
        self.mouse_pos = mouse_pos
        self.draw_radius = draw_radius

    @abstractmethod
    def draw(self) -> None:
        pass

    def set_draw_color(self, new_color: pygame.color.Color) -> None:
        self.draw_color = new_color

    def set_mouse_pos(self, new_pos: (int, int)) -> None:
        self.mouse_pos = new_pos

    def set_draw_radius(self, new_radius: int) -> None:
        self.draw_radius = new_radius


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

    def set_sprite_path(self, new_path: str) -> None:
        self.__sprite_path = new_path


class PatternTool(Instrument):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        super().__init__(display, draw_color, mouse_pos, draw_radius)
        self.__figure_type = instruments_settings.PATTERN_TYPE_RECT
        self.__start_pos = None
        self.__new_surface = None

    def draw(self) -> None:
        if pygame.mouse.get_pressed()[0] and self.__figure_type == instruments_settings.PATTERN_TYPE_RECT:

            if self.__start_pos is None:
                self.__start_pos = self.mouse_pos

            width = self.mouse_pos[0] - self.__start_pos[0]
            height = self.mouse_pos[1] - self.__start_pos[1]

            if width > -1 and height > -1:
                self.__new_surface = pygame.Surface((width, height))
                self.display.blit(self.__new_surface, (self.__start_pos[0], self.__start_pos[1]))

                pygame.draw.rect(self.__new_surface,
                                 self.draw_color,
                                 pygame.Rect(self.__start_pos[0], self.__start_pos[1], width, height)
                                 )

            elif width < 1 and height < 1:

                width = abs(width)
                height = abs(height)

                self.__new_surface = pygame.Surface((width, height))
                self.display.blit(self.__new_surface, (self.mouse_pos[0], self.mouse_pos[1]))

                pygame.draw.rect(self.__new_surface,
                                 self.draw_color,
                                 pygame.Rect(self.mouse_pos[0], self.mouse_pos[1], width, height)
                                 )

            elif width > -1 and height < 1:

                height = abs(height)

                self.__new_surface = pygame.Surface((width, height))
                self.display.blit(self.__new_surface, (self.__start_pos[0], self.__start_pos[1] - height))

                pygame.draw.rect(self.__new_surface,
                                 self.draw_color,
                                 pygame.Rect(self.mouse_pos[0], self.mouse_pos[1], width, height)
                                 )

            elif width < 1 and height > -1:

                width = abs(width)

                self.__new_surface = pygame.Surface((width, height))
                self.display.blit(self.__new_surface, (self.__start_pos[0] - width, self.__start_pos[1]))

                pygame.draw.rect(self.__new_surface,
                                 self.draw_color,
                                 pygame.Rect(self.mouse_pos[0], self.mouse_pos[1], width, height)
                                 )

        else:
            self.__start_pos = None

    def set_figure_type(self, new_type) -> None:
        self.__figure_type = new_type