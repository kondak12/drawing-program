from source.MainLoop import MainLoop


class EventHandler:

    def __init__(self, main_loop: MainLoop):
        self.__main_loop = main_loop

    def stop_running(self) -> None:
        self.__main_loop.set_running(False)