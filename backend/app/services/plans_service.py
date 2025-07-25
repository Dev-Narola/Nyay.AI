from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
import datetime

from app.db.session import get_db
from app.db.models.plans import Plans
from app.utils.duration_days import get_duration_days

def create_default_plan(db:Session):
    plan = db.query(Plans).filter(Plans.name == "Free").first()
    if not plan:
        plan = Plans(
            name = "Free", 
            price=0.0, 
            billing_cycle="yearly", 
            features={
                "cases_per_month": 5,
                "ai_suggestions": False, 
                "priority_support": False
            }, 
            duration_days=get_duration_days('yearly'),
            is_active = True, 
        )

        db.add(plan)
        db.commit()
        db.refresh(plan)
    return plan