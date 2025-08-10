import pygame, tkinter

from tkinter import filedialog
from configs import main_settings
from configs.main_settings import CANVAS_SIZE, ZERO_COORDINATES, CANVAS_BOX


class FileHandler:

    def __init__(self, canvas):
        self.__canvas = canvas
        self.__screenshot_box = main_settings.SCREENSHOT_BOX
        self.__screenshot = None
        self.__import_path = None
        self.__export_path = None

    def __check_import_img_size(self, img: pygame.Surface) -> bool:
        width = img.get_width()
        height = img.get_height()

        return (width != CANVAS_SIZE[0] or height != CANVAS_SIZE[1]) and width < CANVAS_SIZE[0]

    def import_file(self) -> None:
        self.__import_path = tkinter.filedialog.askopenfile()

        if self.__import_path is not None:
            try:
                new_surface = pygame.image.load(self.__import_path).convert()
            except pygame.error:
                return

            if self.__check_import_img_size(new_surface):
                x_pos = (CANVAS_SIZE[0] // 2) - (new_surface.get_width() // 2)
            else:
                x_pos = 0

            self.__canvas.blit(
                new_surface,
                (x_pos, 0),
                CANVAS_BOX
            )

    def export_file(self) -> None:
        self.__screenshot = self.__canvas
        shot = pygame.Surface(CANVAS_SIZE)

        shot.blit(
            self.__canvas,
            ZERO_COORDINATES,
            CANVAS_BOX
        )

        self.__export_path = tkinter.filedialog.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension="png",
            initialfile="saved_picture"
        )

        try:
            if self.__export_path is not None:
                pygame.image.save(shot, self.__export_path)

        except (pygame.error, TypeError):
            return