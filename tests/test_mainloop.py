import pytest
import pygame
from source.MainLoop import MainLoop


@pytest.fixture
def main_loop(surface_stub):

    class InputSystemStub:
        def handle_events(self):
            pass

    main_loop = MainLoop(surface_stub)
    main_loop._MainLoop__input_sys = InputSystemStub()
    main_loop._MainLoop__frames = 60
    return main_loop

def test_mainloop_init_positive(main_loop):
    assert main_loop.get_running()
    assert main_loop._MainLoop__frames == 60
    assert isinstance(main_loop._MainLoop__input_sys, object)

def test_mainloop_run_negative(main_loop):
    def mock_handle_events():
        raise RuntimeError("Handle error")

    main_loop._MainLoop__input_sys.handle_events = mock_handle_events
    with pytest.raises(RuntimeError):
        main_loop.run()

def test_mainloop_set_running_positive(main_loop):
    main_loop.set_running(False)
    assert not main_loop.get_running()
