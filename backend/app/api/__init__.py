# app/api/__init__.py

from fastapi import APIRouter
from app.api.v1.routes import router as v1_router

api_router = APIRouter()
api_router.include_router(v1_router, prefix="/api/v1")
