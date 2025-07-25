from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
import datetime

from app.db.models.refresh_token import RefreshToken
from app.db.session import get_db
from app.db.base_model import response
from app.db.models.user import User
from app.core.security import verify_password, hash_password
from app.core.tokens import create_access_token, generate_refresh_token, hash_token, get_refresh_token_expiry
from app.services.plans_service import create_default_plan

def regestration(name:str, email: str, password:str, mobile:str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user :
        return response(400, "Email already registered")
    
    hashed_password = hash_password(password)

    plan = create_default_plan(db=db)

    user = User(
        name=name,
        email=email,
        password=hashed_password,
        mobile=mobile,
        is_active=True,
        is_email_verified=False,
        is_mobile_verified=False,
        mobile_otp = '000000',
        email_otp = '000000',
        otp_expires_at = datetime.datetime.now(),
        last_login = datetime.datetime.now(),
        created_at=datetime.datetime.now(),

        current_plan_id = plan.id,
        subscription_expiry = datetime.datetime.now() + datetime.timedelta(days=int(plan.duration_days))
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token({"sub" : str(user.id)})
    ref_token = generate_refresh_token()
    hashed_refresh_token = hash_token(ref_token)

    token_obj = refresh_token(user.id, hashed_refresh_token, get_refresh_token_expiry())

    db.add(token_obj)
    db.commit()
    return response(200, "Data created Successfully", [{
            "access_token" : access_token,
            "refresh_token" : ref_token,
            "token_type" : "bearer"
        }])

def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email, User.is_active == True).first()

    if not user or not verify_password(password, user.password):
        return response(401, "Invalid email or password")
    
    access_token = create_access_token({"sub":user.id})
    raw_refresh_token = generate_refresh_token()
    hashed_refresh_token = hash_token(raw_refresh_token)
    expires_at = get_refresh_token_expiry()

    db_token = refresh_token(user.id, hashed_refresh_token, expires_at)

    db.add(db_token)
    db.commit()
    return response(200, "Login successfully", {"access_token" : access_token, "refresh_token" : raw_refresh_token, "token_type" : "bearer"})

def refresh_token(id:str, ref_token:str, expires_at:datetime, device_info:str = "Unknown", is_revoked:bool = False, created_at:datetime = datetime.datetime.now()):
    return RefreshToken(user_id = id, token = ref_token, expires_at= expires_at, created_at = created_at, is_revoked = is_revoked, device_info = device_info, last_used_at=datetime.datetime.utcnow())