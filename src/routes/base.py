from fastapi import FastAPI, APIRouter, Depends
from helpers.config import get_settings,Settings


base_router = APIRouter()
@base_router.get("/")
async def welcome( settings: Settings = Depends(get_settings)):
    app_name=settings.APP_NAME
    version=settings.VERSION
    return {"message": f"Welcome to {app_name}! (Version: {version})"}