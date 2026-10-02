from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str
    VERSION: str
    valid_file_types: List[str]
    mongodb_url: str
    mongodb_database: str

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()        