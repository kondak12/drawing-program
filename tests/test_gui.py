import pytest, pygame

from source.gui import GUIZone, ColorButton, InstrumentButton, LineSizeButton


@pytest.fixture
def gui_zone(surface_stub):
    return GUIZone(surface_stub, 100, 100)

@pytest.fixture
def canvas_manager_stub(hand_stub):
    class CanvasManagerStub:
        def __init__(self):
            self.hand = hand_stub
        def get_hand(self):
            return self.hand
    return CanvasManagerStub()

def test_guizone_init_positive(gui_zone):
    assert gui_zone._GUIZone__width == 100
    assert gui_zone._GUIZone__height == 100

def test_guizone_place_positive(gui_zone):
    def mock_draw_rect(surface, color, rect):
        gui_zone.draw_called = True
    pygame.draw.rect = mock_draw_rect
    gui_zone.draw_called = False
    gui_zone.place((0, 0))
    assert gui_zone.draw_called
    pygame.draw.rect = lambda s, c, r: None

def test_guizone_place_negative(gui_zone):
    def mock_draw_rect(surface, color, rect):
        raise ValueError("Draw error")
    pygame.draw.rect = mock_draw_rect
    with pytest.raises(ValueError):
        gui_zone.place((0, 0))
    pygame.draw.rect = lambda s, c, r: None

@pytest.fixture
def color_button(surface_stub, canvas_manager_stub):
    return ColorButton(50, 50, surface_stub, canvas_manager_stub)

def test_colorbutton_place_current_color_positive(color_button):
    def mock_draw_rect(surface, color, rect):
        color_button.draw_called = True
    pygame.draw.rect = mock_draw_rect
    color_button.draw_called = False
    color_button.place_current_color()
    assert color_button.draw_called
    pygame.draw.rect = lambda s, c, r: None

def test_colorbutton_place_current_color_negative(color_button):

    def mock_draw_rect(surface, color, rect):
        raise ValueError("Draw error")

    pygame.draw.rect = mock_draw_rect
    with pytest.raises(ValueError):
        color_button.place_current_color()
    pygame.draw.rect = lambda s, c, r: None

@pytest.fixture
def instrument_button(surface_stub, canvas_manager_stub):
    return InstrumentButton(50, 50, surface_stub, canvas_manager_stub)

def test_instrumentbutton_place_current_instrument_negative(instrument_button):
    instrument_button._canvas_manager.get_hand().get_main_instrument_type = lambda: (_ for _ in ()).throw(KeyError("Type error"))
    with pytest.raises(KeyError):
        instrument_button.place_current_instrument()

@pytest.fixture
def line_size_button(surface_stub, canvas_manager_stub):
    return LineSizeButton(50, 50, surface_stub, canvas_manager_stub)