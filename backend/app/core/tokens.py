import os
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv(dotenv_path= r"D:\All_Projects\NyayAI\backend\.env")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30))


# ============================
# 🔐 ACCESS TOKEN (JWT)
# ============================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# ============================
# 🔁 REFRESH TOKEN
# ============================

def generate_refresh_token() -> str:
    """Returns a secure plain refresh token to send to the client"""
    return secrets.token_urlsafe(64)


def hash_token(token: str) -> str:
    """Hash refresh token before saving to DB"""
    return hashlib.sha256(token.encode()).hexdigest()


def get_refresh_token_expiry() -> datetime:
    """Returns refresh token expiry timestamp"""
    return datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
