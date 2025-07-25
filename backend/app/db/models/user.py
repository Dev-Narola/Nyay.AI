from sqlalchemy import Boolean, Column, ForeignKey, String, Enum, DateTime, UniqueConstraint
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from ..base import Base
class UserRoleEnum(str):
    USER = "user"
    ADMIN = "admin"
    LAWYER = "lawyer"

class User(Base):
    __tablename__ = "users"
    # __table_args__ = (
    #     UniqueConstraint("email", name="uq_user_email"),
    #     UniqueConstraint("mobile", name="uq_user_mobile"),
    # )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable = False)
    email = Column(String, nullable = False, unique=True, index=True)
    password = Column(String, nullable=False)
    mobile = Column(String, nullable=False, index=True)

    is_email_verified = Column(Boolean, default=True)
    is_mobile_verified = Column(Boolean, default=True)
    email_otp = Column(String, nullable=False)
    mobile_otp = Column(String, nullable=False)
    otp_expires_at = Column(DateTime, nullable=False)

    role = Column(Enum(UserRoleEnum.USER, UserRoleEnum.ADMIN, UserRoleEnum.LAWYER, name="user_roles"), default=UserRoleEnum.USER, nullable=False)
    language_pref = Column(String, default='en', nullable=False)
    is_active = Column(Boolean, nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    current_plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id"), nullable=True)
    subscription_expiry = Column(DateTime, nullable=True)
