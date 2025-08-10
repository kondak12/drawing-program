import pygame

from source.InputSystem import InputSystem
import configs.main_settings, configs.colors


class MainLoop:

    def __init__(self, display: pygame.Surface):
        self.__running = True
        self.__frames = configs.main_settings.FPS
        self.__display = display
        self.__input_sys = InputSystem(self.__display)

    def run(self) -> None:
        while self.__running:

            pygame.time.Clock().tick(self.__frames)

            self.__input_sys.handle_events()

    def get_running(self) -> bool:
        return self.__running

    def set_running(self, new_status: bool) -> None:
        self.__running = new_status