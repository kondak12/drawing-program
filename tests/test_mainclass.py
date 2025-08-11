import pytest
from source.MainClass import MainClass


@pytest.fixture
def main_class(surface_stub):
    class MainLoopStub:

        def run(self):
            pass

    main = MainClass()
    main._MainClass__screen = surface_stub
    main._MainClass__main_loop = MainLoopStub()
    return main

def test_mainclass_init_negative(main_class):
    with pytest.raises(AttributeError):
        del main_class._MainClass__caption
        assert main_class._MainClass__caption

def test_mainclass_run_negative(main_class):
    class MainLoopStub:

        def run(self):
            raise RuntimeError("Loop error")

    main_class._MainClass__main_loop = MainLoopStub()
    with pytest.raises(RuntimeError):
        main_class.run()