from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, base_url):
        self.base_url = base_url
    @abstractmethod
    def scrape(self, identifier):
        pass
    @abstractmethod
    def get_data(self, url):
        pass