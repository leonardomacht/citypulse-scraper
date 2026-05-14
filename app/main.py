import asyncio
from contextlib import asynccontextmanager
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import router
from app.core.browser import browser_manager
from app.core.config import settings
from app.core.database import db_manager    
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.scrappers.manager import scraper_manager
from app.services.corte_service import CorteService

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def scheduled_scraping_task():
    print(f"Iniciando scraping programado a las 02:00 AM...")
    browser = await browser_manager.get_browser()
    data = await scraper_manager.run_scraper("acuacar", browser)
    await CorteService.process_corte(data)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando recursos...")
    await db_manager.connect()

    if not settings.DEBUG:
        await browser_manager.start()
    
    scheduler = AsyncIOScheduler()
    
    trigger = CronTrigger(hour=2, minute=0)
    
    scheduler.add_job(
        scheduled_scraping_task,
        trigger=trigger,
        id="city_pulse_daily_job",
        replace_existing=True
    )

    
    yield  

    print("Cerrando recursos...")
    if not settings.DEBUG:
        await browser_manager.stop()
    await db_manager.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

    