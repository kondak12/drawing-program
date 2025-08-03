import pygame

from source import Instruments
from configs import colors, main_settings, instruments_settings


class Hand:

    def __init__(self, drawing_surface, sprite_path=None):
        self.__drawing_surface = drawing_surface
        self.__sprite_path = sprite_path
        self.__main_color = colors.BLACK
        self.__line_size = 30
        self.__mouse_pos = pygame.mouse.get_pos()
        self.__main_instrument = Instruments.BrushTool(self.__drawing_surface,
                                                       self.__main_color,
                                                       self.__mouse_pos,
                                                       self.__line_size,
                                                       self.__sprite_path
                                                       )

    def update_position(self) -> None:
        self.__mouse_pos = pygame.mouse.get_pos()
        self.__main_instrument.set_mouse_pos(pygame.mouse.get_pos())

    def in_display_borders(self) -> bool:
        return main_settings.SCREEN_SIZE[0] - 100 <= self.__mouse_pos[0]

    def draw(self) -> None:
        if not self.in_display_borders():
            self.__main_instrument.draw()

    def wash_draw(self) -> None:
        if not self.in_display_borders() and pygame.mouse.get_pressed()[2]:
                pygame.draw.circle(self.__drawing_surface,
                                   main_settings.BG_COLOR,
                                   pygame.mouse.get_pos(),
                                   self.__line_size
                                   )

    def __replace_on_brush_tool(self) -> None:
        self.__main_instrument = Instruments.BrushTool(
            self.__drawing_surface,
            self.__main_color,
            pygame.mouse.get_pos(),
            self.__line_size,
            self.__sprite_path
        )

    def __replace_on_pattern_rect_tool(self) -> None:
        self.__main_instrument = Instruments.PatternTool(
            self.__drawing_surface,
            self.__main_color,
            pygame.mouse.get_pos(),
            self.__line_size,
            instruments_settings.PATTERN_TYPE_RECT
        )

    def __replace_on_pattern_circle_tool(self) -> None:
        self.__main_instrument = Instruments.PatternTool(
            self.__drawing_surface,
            self.__main_color,
            pygame.mouse.get_pos(),
            self.__line_size,
            instruments_settings.PATTERN_TYPE_CIRCLE
        )

    def __replace_on_fill_tool(self) -> None:
        self.__main_instrument = Instruments.FillTool(
            self.__drawing_surface,
            self.__main_color,
            pygame.mouse.get_pos(),
            self.__line_size
        )

    def get_main_color(self) -> colors.color:
        return self.__main_color

    def get_main_instrument(self) -> Instruments.Instrument:
        return self.__main_instrument

    def get_line_size(self) -> int:
        return self.__line_size

    def get_sprite_path(self) -> str:
        return self.__sprite_path

    def set_main_color(self, new_color: colors.color) -> None:
        self.__main_instrument.set_draw_color(new_color)
        self.__main_color = new_color

    def set_main_instrument(self, new_instrument) -> None:
        tool_dict = {
            instruments_settings.BRUSH_TOOL: self.__replace_on_brush_tool,
            instruments_settings.FILL_TOOL: self.__replace_on_fill_tool,
            instruments_settings.PATTERN_TOOL_RECT: self.__replace_on_pattern_rect_tool,
            instruments_settings.PATTERN_TOOL_CIRCLE: self.__replace_on_pattern_circle_tool
        }

        tool_dict[new_instrument]()

    def set_line_size(self, new_size: int) -> None:
        self.__main_instrument.set_draw_radius(new_size)
        self.__line_size = new_size

    def set_sprite_path(self, new_sprite_path) -> None:
        self.__main_instrument.set_sprite_path(new_sprite_path)
        self.__sprite_path = new_sprite_path