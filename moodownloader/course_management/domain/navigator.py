from abc import ABC, abstractmethod
from typing import List

from .element import Element

class Navigator(ABC):
    @abstractmethod
    def get_course_links(self) -> List["Element"]:
        pass

    @abstractmethod
    def navigate_to_course(self, course_link) -> None:
        pass