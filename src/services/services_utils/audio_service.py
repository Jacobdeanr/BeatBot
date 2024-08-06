from abc import ABC, abstractmethod
from typing import Optional

class AudioService(ABC):

    @abstractmethod
    def perform_search(self, query: str) -> Optional[str]:
        pass

    @abstractmethod
    def download_song(self, url: str, id: str, duration: int) -> Optional[str]:
        pass
