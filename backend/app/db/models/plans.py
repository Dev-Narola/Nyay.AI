from sqlalchemy import Boolean, Column, String, Enum, DateTime, UniqueConstraint, CheckConstraint, Numeric
import uuid
import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from ..base import Base

import enum

class PlanNameEnum(str, enum.Enum):
    FREE = "Free"
    PRO = "Pro"
    ENTERPRISE = "Enterprise"


class Plans(Base):
    __tablename__ = "plans"
    # __table_args__ = (
    #     UniqueConstraint("name", name="uq_plan_name"),
    #     CheckConstraint("billing_cycle IN ('monthly', 'yearly')", name="chk_billing_cycle"),
    # )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)
    billing_cycle = Column(String(10), nullable=False)
    duration_days = Column(Numeric(10, 2), nullable = False)
    features = Column(JSONB, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
