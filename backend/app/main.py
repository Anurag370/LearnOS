from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.database import AsyncSessionLocal, engine 

from app.api.course import router as course_router
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.learning_goals import router as learning_goals_router
from app.api.learning_plans import router as learning_plans_router

import logging
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("learnos")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s", settings.app_name)
    yield
    logger.info("Shutting down %s", settings.app_name)

    await engine.dispose()

app = FastAPI(
    title= settings.app_name,
    version="0.1.0",
    description="Learning Management System",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course_router, prefix=settings.api_v1_prefix)
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(profile_router, prefix=settings.api_v1_prefix)
app.include_router(learning_goals_router, prefix=settings.api_v1_prefix,)
app.include_router(learning_plans_router, prefix=settings.api_v1_prefix)

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