from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import MongoDsn
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "CityPulse API"
    DEBUG: bool = False
    PORT: int = 8000
    HOST: str = "localhost"
    
    MONGO_URI: str  
    DATABASE_NAME: str = "citypulse"
    

    #SCRAPE_INTERVAL_MINUTES: int = 60
    HEADLESS_BROWSER: bool = True

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" 
    )


settings = Settings()