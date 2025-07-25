# app/api/v1/routes.py

from fastapi import APIRouter
from app.api.v1.auth import router as auth_router

router = APIRouter()
router.include_router(auth_router)  # ✅ Register /api/v1/auth/*
