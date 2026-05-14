from typing import Dict, Type
from app.scrappers.base import BaseScraper
from app.scrappers.acuacar import AcuacarScraper

class ScraperManager:
    def __init__(self):
        self._scrapers: Dict[str, Type[BaseScraper]] = {
            "acuacar": AcuacarScraper,
        }

    async def run_scraper(self, service_name: str, browser):
        scraper_class = self._scrapers.get(service_name.lower())
        
        if not scraper_class:
            raise ValueError(f"El servicio '{service_name}' no está soportado.")
        
        scraper = scraper_class()
        print(f"Iniciando scraping para: {service_name}")
        return await scraper.scrape(browser)

    async def run_all(self, browser):
        results = {}
        for name in self._scrapers.keys():
            try:
                results[name] = await self.run_scraper(name, browser)
            except Exception as e:
                print(f"Error scrapeando {name}: {e}")
        return results

scraper_manager = ScraperManager()