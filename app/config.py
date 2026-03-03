from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "ecommerce_shipping"

    class Config:
        env_file = ".env"


# Singleton pattern for settings
settings = Settings()
