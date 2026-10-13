from tkinter import N

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str
    VERSION: str
    valid_file_types: List[str]
    mongodb_url: str
    mongodb_database: str
    # ===========================================================    
    OPENAI_API_KEY: str
    OPENAI_API_URL: str
    COHERE_API_KEY: str
    
    GENERATION_MODEL_ID: str
    GENERATION_MODEL_NAME:str
    
    
    EMBEDDING_MODEL_ID: str
    EMBEDDING_MODEL_NAME:str
    EMBEDDING_MODEL_SIZE: int

    INPUT_DEFAULT_MAX_CHARACTERS: int
    GENERATION_DEFAULT_MAX_TOKENS: int
    GENERATION_DEFAULT_TEMPERATURE: float
    
    # ===========================================================
    VECTOR_DB_TYPE:str
    VECTOR_DB_DISTANCE_METHOD:str
    VECTOR_DB_NAME:str
    # =====================
    DEFAULT_LANGUAGE:str
    PRIME_LANGUAGE:str

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()        