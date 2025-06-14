from abc import ABC, abstractmethod

class InputSource(ABC):
    @abstractmethod
    def read(self) -> dict:
        """Returns raw input values as a dict (e.g. {'axis_1': float, 'button_0': int})"""
        pass
