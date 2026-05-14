from fastapi import APIRouter, Depends
from app.scrappers.manager import scraper_manager
from app.core.browser import browser_manager
from app.core.database import db_manager
from app.services.corte_service import CorteService

router = APIRouter()

@router.post("/scrape/{service}")
async def force_scrape(service: str):
    try:
        browser = await browser_manager.get_browser()
        data = await scraper_manager.run_scraper(service, browser)
        id = await CorteService.process_corte(data)
        return {"message": "Corte guardado", "id": id}
    except ValueError as e:
        return {"status": "error", "message": str(e)}