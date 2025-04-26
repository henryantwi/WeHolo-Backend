from sqlalchemy import Boolean, Column, String, Integer, DateTime, ForeignKey, Text, Float, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.models.base import Base

class SubscriptionType(enum.Enum):
    BASIC = "basic"  # AKOOL features
    PREMIUM = "premium"  # Soul Machines features

class Subscription(Base):
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(SubscriptionType), nullable=False)
    price = Column(Float, nullable=False)

    # Billing period in months
    billing_period = Column(Integer, default=1)

    # Subscription status
    is_active = Column(Boolean, default=True)

    # Subscription dates
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True))

    # Payment information
    payment_method = Column(String)
    payment_id = Column(String)

    # User relationship
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="subscriptions")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
