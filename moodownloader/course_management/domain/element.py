from abc import ABC, abstractmethod
from typing import List, Dict

class Element(ABC):
    text: str

    @abstractmethod
    def find_all(self, tag: str, params: Dict[any]) -> List["Element"]:
        pass

    @abstractmethod
    def __getattr__(self, name: str) -> any:
        pass

    @abstractmethod
    def __setattr__(self, name: str, value: any) -> None:
        pass