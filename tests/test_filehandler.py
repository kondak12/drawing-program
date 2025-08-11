import pytest, pygame, tkinter

from source.FileHandler import FileHandler
import configs.main_settings as main_settings
from stubs import SurfaceStub

@pytest.fixture
def file_handler(surface_stub):
    return FileHandler(surface_stub)

def test_filehandler_init_positive(file_handler):
    assert file_handler._FileHandler__screenshot_box == main_settings.SCREENSHOT_BOX

def test_filehandler_import_file_positive(file_handler):
    def mock_askopenfile():
        return "test.png"
    tkinter.filedialog.askopenfile = mock_askopenfile

    def mock_load(path):
        return SurfaceStub((100, 100))
    pygame.image.load = mock_load

    def mock_blit(source, dest, area):
        file_handler.blit_called = True
    file_handler._FileHandler__canvas.blit = mock_blit
    file_handler.blit_called = False
    file_handler.import_file()

    assert file_handler.blit_called

    tkinter.filedialog.askopenfile = lambda: None
    pygame.image.load = lambda p: SurfaceStub()
    file_handler._FileHandler__canvas.blit = lambda src, dest, area: None

def test_filehandler_import_file_negative(file_handler):
    def mock_askopenfile():
        return "test.png"

    tkinter.filedialog.askopenfile = mock_askopenfile

    def mock_load(path):
        raise pygame.error("Load error")

    pygame.image.load = mock_load

    def mock_blit(source, dest, area):
        file_handler.blit_called = True

    file_handler._FileHandler__canvas.blit = mock_blit
    file_handler.blit_called = False
    file_handler.import_file()

    assert not file_handler.blit_called

    tkinter.filedialog.askopenfile = lambda: None
    pygame.image.load = lambda p: SurfaceStub()

def test_filehandler_export_file_positive(file_handler):

    def mock_asksaveasfilename(**kwargs):
        return "saved.png"

    tkinter.filedialog.asksaveasfilename = mock_asksaveasfilename

    def mock_save(surface, path):
        file_handler.save_called = True

    pygame.image.save = mock_save
    file_handler.save_called = False

    def mock_surface(size):
        return SurfaceStub(size)

    pygame.Surface = mock_surface
    file_handler.export_file()
    assert file_handler.save_called
    tkinter.filedialog.asksaveasfilename = lambda **kwargs: None
    pygame.image.save = lambda s, p: None
    pygame.Surface = lambda size: SurfaceStub(size)

def test_filehandler_export_file_negative(file_handler):
    def mock_asksaveasfilename(**kwargs):
        return "saved.png"
    tkinter.filedialog.asksaveasfilename = mock_asksaveasfilename

    def mock_save(surface, path):
        raise pygame.error("Save error")

    pygame.image.save = mock_save

    def mock_surface(size):
        return SurfaceStub(size)

    pygame.Surface = mock_surface
    file_handler.export_file()

    tkinter.filedialog.asksaveasfilename = lambda **kwargs: None
    pygame.image.save = lambda s, p: None
    pygame.Surface = lambda size: SurfaceStub(size)