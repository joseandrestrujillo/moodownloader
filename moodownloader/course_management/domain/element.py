from abc import ABC, abstractmethod
from typing import List, Dict

class Element(ABC):
    text: str

    @abstractmethod
    def find_all(self, tag: str, params: Dict) -> List["Element"]:
        pass

    @abstractmethod
    def find(self, tag: str, params: Dict) -> "Element":
        pass

    @abstractmethod
    def __getattr__(self, name: str) -> any:
        pass
