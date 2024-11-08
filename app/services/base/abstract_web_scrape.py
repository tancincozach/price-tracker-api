from abc import ABC, abstractmethod

class AbstractWebScraper(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def fetch(self, endpoint: str, data: dict = None):
        pass  # The subclass will implement this method
    def build_url(self, segments: str):
        pass  # The subclass will implement this method
