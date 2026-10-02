

from fastapi import FastAPI

from helpers.config import get_settings,Settings
from motor.motor_asyncio import AsyncIOMotorClient       
from routes import base,data
app=FastAPI()
@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_connection = AsyncIOMotorClient(settings.mongodb_url)
    app.db_client = app.mongodb_connection[settings.mongodb_database]

app.include_router(base.base_router) 
app.include_router(data.data_router)
