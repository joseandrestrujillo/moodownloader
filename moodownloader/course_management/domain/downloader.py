from abc import ABC, abstractmethod

class Downloader(ABC):
    @abstractmethod
    def download_all_pdfs(self) -> None:
        pass