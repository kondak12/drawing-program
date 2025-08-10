from abc import ABC, abstractmethod
import pygame

from configs import main_settings


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

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        super().__init__(display, draw_color, mouse_pos, draw_radius)
        self.__last_pos = None

    def draw(self) -> None:
        if pygame.mouse.get_pressed()[0]:

            if self.__last_pos:

                dist_x = self.mouse_pos[0] - self.__last_pos[0]
                dist_y = self.mouse_pos[1] - self.__last_pos[1]
                distance = max(1, int((dist_x ** 2 + dist_y ** 2) ** 0.5))

                for i in range(distance):
                    x = int(self.__last_pos[0] + dist_x * i / distance)
                    y = int(self.__last_pos[1] + dist_y * i / distance)
                    pygame.draw.circle(self.display, self.draw_color, (x, y), self.draw_radius // 2)
            self.__last_pos = self.mouse_pos

        else:
            self.__last_pos = None


class FillTool(Instrument):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        super().__init__(display, draw_color, mouse_pos, draw_radius)
        self.__x_pos = mouse_pos[0]
        self.__y_pos = mouse_pos[1]
        self.__bottom_layer = None

    def set_bottom_layer(self) -> None:
        self.__bottom_layer = pygame.Surface.get_at(self.display, self.mouse_pos)

    def draw(self) -> None:
        if pygame.mouse.get_pressed()[0] == 1:
            self.set_bottom_layer()

            if self.__bottom_layer == self.draw_color:
                return

            stack = [self.mouse_pos]

            while stack:
                current_pixel = stack.pop()

                if pygame.Surface.get_at(self.display, current_pixel) == self.__bottom_layer:
                    pygame.Surface.set_at(self.display, current_pixel, self.draw_color)

                    if current_pixel[0] + 1 < main_settings.CANVAS_SIZE[0]:
                        stack.append((current_pixel[0] + 1, current_pixel[1]))

                    if current_pixel[0] - 1 >= 0:
                        stack.append((current_pixel[0] - 1, current_pixel[1]))

                    if current_pixel[1] + 1 < main_settings.CANVAS_SIZE[1]:
                        stack.append((current_pixel[0], current_pixel[1] + 1))

                    if current_pixel[1] - 1 >= 0:
                        stack.append((current_pixel[0], current_pixel[1] - 1))


class PatternTool(Instrument):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        super().__init__(display, draw_color, mouse_pos, draw_radius)
        self._start_pos = None
        self._background = None
        self._new_surface = None

    @abstractmethod
    def _create_new_surface(self, width, height) -> pygame.Surface:
        pass

    def draw(self) -> None:
        if pygame.mouse.get_pressed()[0]:

            if self.__start_pos is None:
                self.__start_pos = self.mouse_pos

                self.__background = self.display.copy()

            self.display.blit(self.__background, main_settings.ZERO_COORDINATES)

            x0, y0 = self.__start_pos
            x1, y1 = self.mouse_pos
            width  = x1 - x0
            height = y1 - y0

            if width >= 0 and height >= 0:
                dest = (x0, y0)

            elif width < 0 and height < 0:
                dest = (x1, y1)
                width, height = -width, -height

            elif width >= 0 and height < 0:
                dest = (x0, y1)
                height = -height

            else:
                dest = (x1, y0)
                width = -width

            self.__new_surface = self._create_new_surface(width, height)
            self.display.blit(self.__new_surface, dest)

        else:
            self.__start_pos = None
            self.__background = None
            self.__new_surface = None


class RectPatternTool(PatternTool):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        super().__init__(display, draw_color, mouse_pos, draw_radius)

    def _create_new_surface(self, width, height) -> pygame.Surface:
        surf = pygame.Surface((width, height), pygame.SRCALPHA)

        pygame.draw.rect(
            surf,
            self.draw_color,
            pygame.Rect(0, 0, width, height),
            self.draw_radius
        )

        return surf


class CirclePatternTool(PatternTool):

    def __init__(self, display, draw_color, mouse_pos, draw_radius):
        super().__init__(display, draw_color, mouse_pos, draw_radius)

    def _create_new_surface(self, width, height) -> pygame.Surface:
        surf = pygame.Surface((width, height), pygame.SRCALPHA)

        pygame.draw.ellipse(
            surf,
            self.draw_color,
            (0, 0, width, height),
            self.draw_radius
        )

        return surf