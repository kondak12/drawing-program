import pytest, pygame
from source.Instruments import BrushTool, FillTool, RectPatternTool


@pytest.fixture
def brush_tool(surface_stub):
    return BrushTool(surface_stub, pygame.Color('black'), (0, 0), 5)

def test_instrument_set_draw_color_positive(brush_tool):
    new_color = pygame.Color('red')
    brush_tool.set_draw_color(new_color)
    assert brush_tool.draw_color == new_color

def test_instrument_set_mouse_pos_positive(brush_tool):
    new_pos = (100, 100)
    brush_tool.set_mouse_pos(new_pos)
    assert brush_tool.mouse_pos == new_pos

def test_instrument_set_draw_radius_positive(brush_tool):
    new_radius = 10
    brush_tool.set_draw_radius(new_radius)
    assert brush_tool.draw_radius == new_radius

def test_brushtool_draw_positive(surface_stub):
    brush = BrushTool(surface_stub, pygame.Color('black'), (0, 0), 5)
    brush._BrushTool__last_pos = (0, 0)
    brush.mouse_pos = (10, 10)

    def mock_get_pressed():
        return (True, False, False)

    pygame.mouse.get_pressed = mock_get_pressed

    def mock_draw_circle(surface, color, pos, radius):
        brush.draw_called = True

    pygame.draw.circle = mock_draw_circle
    brush.draw_called = False
    brush.draw()
    assert brush.draw_called
    pygame.mouse.get_pressed = lambda: (False, False, False)
    pygame.draw.circle = lambda s, c, p, r: None

def test_brushtool_draw_negative(surface_stub):
    brush = BrushTool(surface_stub, pygame.Color('black'), (0, 0), 5)

    def mock_get_pressed():
        return (False, False, False)

    pygame.mouse.get_pressed = mock_get_pressed
    brush.draw()
    assert brush._BrushTool__last_pos is None
    pygame.mouse.get_pressed = lambda: (False, False, False)

def test_brushtool_wash_draw_positive(surface_stub):
    brush = BrushTool(surface_stub, pygame.Color('black'), (0, 0), 5)
    brush._BrushTool__last_pos = (0, 0)
    brush.mouse_pos = (10, 10)

    def mock_get_pressed():
        return (False, False, True)

    pygame.mouse.get_pressed = mock_get_pressed

    def mock_draw_circle(surface, color, pos, radius):
        brush.wash_draw_called = True

    pygame.draw.circle = mock_draw_circle
    brush.wash_draw_called = False
    brush.wash_draw()
    assert brush.wash_draw_called
    pygame.mouse.get_pressed = lambda: (False, False, False)
    pygame.draw.circle = lambda s, c, p, r: None

def test_filltool_draw_negative(surface_stub):
    fill = FillTool(surface_stub, pygame.Color('black'), (10, 10), 5)

    def mock_get_pressed():
        return (True, False, False)

    pygame.mouse.get_pressed = mock_get_pressed
    fill._FillTool__in_canvas = lambda: True
    surface_stub.color = pygame.Color('black')
    original_color = surface_stub.color
    fill.draw()
    assert surface_stub.color == original_color
    pygame.mouse.get_pressed = lambda: (False, False, False)

def test_patterntool_draw_negative(surface_stub):
    pattern = RectPatternTool(surface_stub, pygame.Color('black'), (0, 0), 5)

    def mock_get_pressed():
        return (False, False, False)

    pygame.mouse.get_pressed = mock_get_pressed
    pattern.draw()
    assert pattern._start_pos is None
    pygame.mouse.get_pressed = lambda: (False, False, False)