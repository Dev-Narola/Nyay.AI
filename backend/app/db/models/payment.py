import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    String,
    ForeignKey,
    Numeric,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from ..base import Base

class PaymentStatusEnum(str):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"

class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        CheckConstraint("status IN ('success', 'failed', 'pending')", name="chk_payment_status"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id", ondelete="SET NULL"), nullable=True)

    amount = Column(Numeric(10, 2), nullable=False)

    payment_method = Column(String(50), nullable=True)
    payment_id = Column(String(100), nullable=True)

    status = Column(String(10), default=PaymentStatusEnum.PENDING, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
