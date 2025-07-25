import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
    String,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from ..base import Base

class PaymentStatusEnum(str):
    PAID = "paid"
    FAILED = "failed"
    PENDING = "pending"

class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        CheckConstraint(
            "payment_status IN ('paid', 'failed', 'pending')",
            name="chk_payment_status"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id"), nullable=False)

    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=False)

    is_active = Column(Boolean, default=True)
    cancelled_at = Column(DateTime, nullable=True)

    payment_status = Column(String(10), default=PaymentStatusEnum.PENDING, nullable=False)
