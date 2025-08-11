import pytest, pygame

from source.InputSystem import InputSystem
import configs.main_settings as main_settings
from stubs import SurfaceStub  # Добавляем импорт


@pytest.fixture
def input_system(surface_stub, hand_stub):
    class CanvasManagerStub:
        def __init__(self):
            self.canvas = surface_stub
            self.hand = hand_stub
            self.place_called = False
            self.cycle_called = False

        def place_gui_on_screen(self, event):
            self.place_called = True

        def do_action_screen_cycle(self, event):
            self.cycle_called = True

        def get_hand(self):
            return self.hand

    input_sys = InputSystem(surface_stub)
    input_sys._InputSystem__canvas = CanvasManagerStub()
    input_sys._InputSystem__hand = hand_stub
    input_sys._InputSystem__gui = SurfaceStub(main_settings.GUI_REGION_SIZE)
    return input_sys

def test_inputsystem_init_positive(input_system, surface_stub):
    assert isinstance(input_system._InputSystem__gui, SurfaceStub)
    assert input_system._InputSystem__surface == surface_stub
    assert input_system._InputSystem__hand == input_system._InputSystem__canvas.get_hand()

def test_inputsystem_handle_events_negative(input_system):
    def mock_event_get():
        raise RuntimeError("Event error")
    pygame.event.get = mock_event_get
    with pytest.raises(RuntimeError):
        input_system.handle_events()
    pygame.event.get = lambda: []