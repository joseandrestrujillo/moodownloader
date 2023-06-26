from abc import ABC, abstractmethod

class Authenticator(ABC):
    @abstractmethod
    def authenticate(self) -> bool:
        pass