import pytest, pygame

import configs.main_settings as main_settings
import configs.colors as colors
import configs.instruments_settings as instruments_settings

@pytest.fixture
def hand(surface_stub):

    class BrushToolStub:

        def __init__(self, surface, color, pos, size):
            self.draw_color = color
            self.mouse_pos = pos
            self.draw_radius = size

        def set_mouse_pos(self, pos):
            self.mouse_pos = pos

        def set_draw_color(self, color):
            self.draw_color = color

        def set_draw_radius(self, radius):
            self.draw_radius = radius

        def draw(self):
            pass

        def wash_draw(self):
            pass

    from source.Hand import Hand

    hand = Hand(surface_stub)
    hand._Hand__main_instrument = BrushToolStub(surface_stub, colors.BLACK, (0, 0), 5)
    hand._Hand__eraser = BrushToolStub(surface_stub, colors.WHITE, (0, 0), 5)
    return hand

def test_hand_init_positive(hand):
    assert hand.get_main_color() == colors.BLACK
    assert hand.get_line_size() == 5
    assert hand.get_sprite_path() is None

def test_hand_update_position_positive(hand):
    def mock_get_pos():
        return (100, 200)

    pygame.mouse.get_pos = mock_get_pos
    hand.update_position()

    assert hand.get_mouse_pos() == (100, 200)
    assert hand._Hand__main_instrument.mouse_pos == (100, 200)
    assert hand._Hand__eraser.mouse_pos == (100, 200)
    pygame.mouse.get_pos = lambda: (0, 0)

def test_hand_update_position_negative(hand):
    def mock_get_pos():
        raise RuntimeError("Mouse error")

    pygame.mouse.get_pos = mock_get_pos
    with pytest.raises(RuntimeError):
        hand.update_position()
    pygame.mouse.get_pos = lambda: (0, 0)

def test_hand_in_gui_borders_positive(hand):
    hand._Hand__mouse_pos = (main_settings.WINDOW_SIZE[0] - 10, 10)
    assert hand.in_gui_borders()

def test_hand_in_gui_borders_negative(hand):
    hand._Hand__mouse_pos = (0, 0)
    assert not hand.in_gui_borders()

def test_hand_set_main_color_positive(hand):
    new_color = colors.RED
    hand.set_main_color(new_color)
    assert hand.get_main_color() == new_color
    assert hand._Hand__main_instrument.draw_color == new_color

def test_hand_set_main_instrument_positive(hand):
    hand.set_main_instrument(instruments_settings.BRUSH_TOOL)
    assert hand.get_main_instrument_type() == instruments_settings.BRUSH_TOOL

def test_hand_set_main_instrument_negative(hand):
    with pytest.raises(KeyError):
        hand.set_main_instrument("invalid_tool")

def test_hand_set_line_size_positive(hand):
    new_size = 10
    hand.set_line_size(new_size)

    assert hand.get_line_size() == new_size
    assert hand._Hand__main_instrument.draw_radius == new_size
    assert hand._Hand__eraser.draw_radius == new_size

def test_hand_get_main_instrument_type_negative(hand):
    hand._Hand__main_instrument = object()
    with pytest.raises(KeyError):
        hand.get_main_instrument_type()