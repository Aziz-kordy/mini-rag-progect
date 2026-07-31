from fastapi import FastAPI, APIRouter
import os

base_router = APIRouter()
@base_router.get("/")
async def welcome():
    app_name=os.getenv("APP_NAME")
    return {"message": f"Welcome to {app_name}!"}