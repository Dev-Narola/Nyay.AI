# app/api/v1/auth.py

from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.services.auth_service import login, regestration
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    return login(email, password, db)

@router.post("/signup")
async def signup(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    mobile = data.get("mobile")

    if not name or not email or not password:
        raise HTTPException(status_code=400, detail="Name, email, and password are required")

    return regestration(name, email, password, mobile, db)
