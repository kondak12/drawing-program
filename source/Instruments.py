from abc import ABC, abstractmethod


class Instrument(ABC):

    @abstractmethod
    def draw(self) -> None:
        pass


class BrushTool(Instrument):

    def draw(self) -> None:
        pass