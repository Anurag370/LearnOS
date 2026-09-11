from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.database import AsyncSessionLocal

app = FastAPI(
    title= settings.app_name,
    version="0.1.0",
    description="Learning Management System",
)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "services": settings.app_name,
    }

@app.get("/health/db")
async def database_health_check():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar_one()

    return {
        "status": "ok",
        "dataabse": "connected",
        "result": value,
    }