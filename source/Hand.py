import pygame

from source import Instruments
from configs import colors, main_settings, instruments_settings


class Hand:

    def __init__(self, drawing_surface, sprite_path=None):
        self.__drawing_surface = drawing_surface
        self.__sprite_path = sprite_path
        self.__main_color = colors.BLACK
        self.__line_size = 5
        self.__mouse_pos = pygame.mouse.get_pos()
        self.__main_instrument = Instruments.BrushTool(
            self.__drawing_surface,
            self.__main_color,
            self.__mouse_pos,
            self.__line_size
        )

    def update_position(self) -> None:
        self.__mouse_pos = pygame.mouse.get_pos()
        self.__main_instrument.set_mouse_pos(pygame.mouse.get_pos())

    def in_gui_borders(self) -> bool:
        gui_x_pos = main_settings.GUI_REGION_POSITION[0]
        gui_y_pos = main_settings.GUI_REGION_SIZE[1]
        window_x_pos = main_settings.WINDOW_SIZE[0]

        return (gui_x_pos <= self.__mouse_pos[0] <= window_x_pos) and (0 <= self.__mouse_pos[1] <= gui_y_pos)

    def draw(self) -> None:
        if not self.in_gui_borders():
            self.__main_instrument.draw()

    def wash_draw(self) -> None:
        if not self.in_gui_borders() and pygame.mouse.get_pressed()[2]:
                pygame.draw.circle(
                    self.__drawing_surface,
                    main_settings.BG_COLOR,
                    self.__mouse_pos,
                    self.__line_size
                )

    def __replace_on_brush_tool(self) -> None:
        self.__main_instrument = Instruments.BrushTool(
            self.__drawing_surface,
            self.__main_color,
            self.__mouse_pos,
            self.__line_size
        )

    def __replace_on_pattern_rect_tool(self) -> None:
        self.__main_instrument = Instruments.RectPatternTool(
            self.__drawing_surface,
            self.__main_color,
            self.__mouse_pos,
            self.__line_size
        )

    def __replace_on_pattern_circle_tool(self) -> None:
        self.__main_instrument = Instruments.CirclePatternTool(
            self.__drawing_surface,
            self.__main_color,
            self.__mouse_pos,
            self.__line_size
        )

    def __replace_on_fill_tool(self) -> None:
        self.__main_instrument = Instruments.FillTool(
            self.__drawing_surface,
            self.__main_color,
            self.__mouse_pos,
            self.__line_size
        )

    def get_main_color(self) -> colors.color:
        return self.__main_color

    def get_main_instrument(self) -> Instruments.Instrument:
        return self.__main_instrument

    def get_main_instrument_type(self) -> str:
        tool_dict = {
            instruments_settings.BRUSH_TOOL: instruments_settings.BRUSH_TOOL,
            instruments_settings.FILL_TOOL: instruments_settings.FILL_TOOL,
            instruments_settings.RECT_TOOL: instruments_settings.RECT_TOOL,
            instruments_settings.CIRCLE_TOOL: instruments_settings.CIRCLE_TOOL
        }

        return tool_dict[f"{type(self.__main_instrument)}"]

    def get_line_size(self) -> int:
        return self.__line_size

    def get_sprite_path(self) -> str:
        return self.__sprite_path

    def get_mouse_pos(self) -> (int, int):
        return self.__mouse_pos

    def set_main_color(self, new_color: colors.color) -> None:
        self.__main_instrument.set_draw_color(new_color)
        self.__main_color = new_color

    def set_main_instrument(self, new_instrument) -> None:
        tool_dict = {
            instruments_settings.BRUSH_TOOL: self.__replace_on_brush_tool,
            instruments_settings.FILL_TOOL: self.__replace_on_fill_tool,
            instruments_settings.RECT_TOOL: self.__replace_on_pattern_rect_tool,
            instruments_settings.CIRCLE_TOOL: self.__replace_on_pattern_circle_tool
        }

        tool_dict[new_instrument]()

    def set_line_size(self, new_size: int) -> None:
        self.__main_instrument.set_draw_radius(new_size)
        self.__line_size = new_size