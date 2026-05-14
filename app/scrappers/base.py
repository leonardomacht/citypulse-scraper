from abc import ABC, abstractmethod
from playwright.async_api import async_playwright

class BaseScraper(ABC):
    @abstractmethod
    async def scrape(self):
        pass