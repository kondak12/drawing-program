import pytest, pygame

from source.CanvasManager import CanvasManager
import configs.main_settings as main_settings
from stubs import SurfaceStub

@pytest.fixture
def canvas_manager(surface_stub, hand_stub):
    gui_surface = SurfaceStub(main_settings.GUI_REGION_SIZE)

    class GUIZoneStub:
        def place(self, pos):
            self.place_called = True

    class ColorButtonStub:
        def place(self, x, y, event, color=None):
            self.place_called = True

        def place_current_color(self):
            self.current_color_called = True

    class InstrumentButtonStub:
        def place(self, x, y, event, caps_img_name=None):
            self.place_called = True

        def place_current_instrument(self):
            self.current_instrument_called = True

    class LineSizeButtonStub:
        def place(self, x, y, event):
            self.place_called = True

    class FunctionButtonStub:
        def place(self, x, y, event, img_name=None, function=None):
            self.place_called = True

    class FileHandlerStub:
        def import_file(self):
            pass

        def export_file(self):
            pass

    manager = CanvasManager(surface_stub, hand_stub, gui_surface)
    manager._CanvasManager__gui_zone = GUIZoneStub()
    manager._CanvasManager__color_btn = ColorButtonStub()
    manager._CanvasManager__instrument_btn = InstrumentButtonStub()
    manager._CanvasManager__line_btn = LineSizeButtonStub()
    manager._CanvasManager__function_btn = FunctionButtonStub()
    manager._CanvasManager__file_handler = FileHandlerStub()

    return manager

def test_canvasmanager_init_positive(canvas_manager):
    assert isinstance(canvas_manager._CanvasManager__gui_zone, object)
    assert isinstance(canvas_manager._CanvasManager__color_btn, object)
    assert canvas_manager._CanvasManager__action_screen_sequence[main_settings.APPROVED_CANVAS_ACTIONS] is not None

def test_canvasmanager_do_action_screen_cycle_negative(canvas_manager):
    class Event:
        type = pygame.MOUSEBUTTONDOWN

    def mock_in_gui_borders():
        return True

    canvas_manager._CanvasManager__hand.in_gui_borders = mock_in_gui_borders
    original_sequence = canvas_manager._CanvasManager__action_screen_sequence.copy()
    canvas_manager.do_action_screen_cycle(Event())

    assert canvas_manager._CanvasManager__action_screen_sequence == original_sequence

def test_canvasmanager_place_gui_on_screen_positive(canvas_manager):
    class Event:
        pass

    canvas_manager._CanvasManager__gui_zone.place_called = False
    canvas_manager._CanvasManager__color_btn.place_called = False
    canvas_manager._CanvasManager__color_btn.current_color_called = False
    canvas_manager._CanvasManager__instrument_btn.place_called = False
    canvas_manager._CanvasManager__instrument_btn.current_instrument_called = False
    canvas_manager._CanvasManager__line_btn.place_called = False
    canvas_manager._CanvasManager__function_btn.place_called = False

    def mock_blit(source, dest):
        canvas_manager.blit_called = True

    canvas_manager._CanvasManager__canvas.blit = mock_blit
    canvas_manager.blit_called = False
    canvas_manager.place_gui_on_screen(Event())
    assert canvas_manager._CanvasManager__gui_zone.place_called
    assert canvas_manager._CanvasManager__color_btn.place_called
    assert canvas_manager._CanvasManager__color_btn.current_color_called
    assert canvas_manager._CanvasManager__instrument_btn.place_called
    assert canvas_manager._CanvasManager__instrument_btn.current_instrument_called
    assert canvas_manager._CanvasManager__line_btn.place_called
    assert canvas_manager._CanvasManager__function_btn.place_called
    assert canvas_manager.blit_called
    canvas_manager._CanvasManager__canvas.blit = lambda src, dest: None

def test_canvasmanager_place_gui_on_screen_negative(canvas_manager):
    class Event:
        pass

    def mock_place(pos):
        raise ValueError("Place error")

    canvas_manager._CanvasManager__gui_zone.place = mock_place

    with pytest.raises(ValueError):
        canvas_manager.place_gui_on_screen(Event())

def test_canvasmanager_get_hand_positive(canvas_manager, hand_stub):
    assert canvas_manager.get_hand() == hand_stub