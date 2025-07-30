from abc import ABC, abstractmethod
import pygame

from configs import main_settings, instruments_settings


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

        if 0 <= self.mouse_pos[0] <= main_settings.CANVAS_BORDERS[0] and 0 <= self.mouse_pos[1] <= main_settings.CANVAS_BORDERS[1]:

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

    def __create_new_surface(self, width, height, dest_x, dest_y) -> None:
        self.__new_surface = pygame.Surface((width, height))

        pygame.draw.rect(self.__new_surface,
                         self.draw_color,
                         pygame.Rect(0, 0, width, height)
                         )

        self.display.blit(self.__new_surface, (dest_x, dest_y))

    def draw(self) -> None:

        if 0 <= self.mouse_pos[0] <= main_settings.CANVAS_BORDERS[0] and 0 <= self.mouse_pos[1] <= main_settings.CANVAS_BORDERS[1]:

            if pygame.mouse.get_pressed()[0] and self.__figure_type == instruments_settings.PATTERN_TYPE_RECT:

                if self.__start_pos is None:
                    self.__start_pos = self.mouse_pos

                width = self.mouse_pos[0] - self.__start_pos[0]
                height = self.mouse_pos[1] - self.__start_pos[1]

                if width > -1 and height > -1:

                    self.__create_new_surface(width, height, self.__start_pos[0], self.__start_pos[1])

                elif width < 1 and height < 1:

                    width = abs(width)
                    height = abs(height)

                    self.__create_new_surface(width, height, self.mouse_pos[0], self.mouse_pos[1])

                elif width > -1 and height < 1:

                    height = abs(height)

                    self.__create_new_surface(width, height, self.__start_pos[0], self.__start_pos[1] - height)

                elif width < 1 and height > -1:

                    width = abs(width)

                    self.__create_new_surface(width, height, self.__start_pos[0] - width, self.__start_pos[1])

            else:
                self.__start_pos = None

    def set_figure_type(self, new_type) -> None:
        self.__figure_type = new_type


class FillTool(Instrument):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        super().__init__(display, draw_color, mouse_pos, draw_radius)
        self.__x_pos = mouse_pos[0]
        self.__y_pos = mouse_pos[1]
        self.__bottom_layer = None

    def set_bottom_layer(self) -> None:
        self.__bottom_layer = pygame.Surface.get_at(self.display, self.mouse_pos)

    def draw(self) -> None:
        if 0 <= self.mouse_pos[0] <= main_settings.CANVAS_BORDERS[0] and 0 <= self.mouse_pos[1] <= main_settings.CANVAS_BORDERS[1]:

            if pygame.mouse.get_pressed()[0] == 1:
                self.set_bottom_layer()

                if self.__bottom_layer == self.draw_color:
                    return

                stack = [self.mouse_pos]

                while stack:
                    current_pixel = stack.pop()

                    if pygame.Surface.get_at(self.display, current_pixel) == self.__bottom_layer:
                        pygame.Surface.set_at(self.display, current_pixel, self.draw_color)

                        if current_pixel[0] + 1 < main_settings.SCREEN_SIZE[0]:
                            stack.append((current_pixel[0] + 1, current_pixel[1]))

                        if current_pixel[0] - 1 >= 0:
                            stack.append((current_pixel[0] - 1, current_pixel[1]))

                        if current_pixel[1] + 1 < main_settings.SCREEN_SIZE[1]:
                            stack.append((current_pixel[0], current_pixel[1] + 1))

                        if current_pixel[1] - 1 >= 0:
                            stack.append((current_pixel[0], current_pixel[1] - 1))