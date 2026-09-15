from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.database import AsyncSessionLocal

from app.api.course import router as course_router

app = FastAPI(
    title= settings.app_name,
    version="0.1.0",
    description="Learning Management System",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course_router)

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
        "database": "connected",
        "result": value,
    }