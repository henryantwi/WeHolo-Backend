from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

class SubscriptionType(str, Enum):
    BASIC = "basic"
    PREMIUM = "premium"

# Shared properties
class SubscriptionBase(BaseModel):
    type: Optional[SubscriptionType] = None
    price: Optional[float] = None
    billing_period: Optional[int] = 1
    is_active: Optional[bool] = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    payment_id: Optional[str] = None

# Properties to receive via API on creation
class SubscriptionCreate(SubscriptionBase):
    type: SubscriptionType
    price: float
    user_id: int

# Properties to receive via API on update
class SubscriptionUpdate(SubscriptionBase):
    pass

# Properties shared by models stored in DB
class SubscriptionInDBBase(SubscriptionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class Subscription(SubscriptionInDBBase):
    pass

# Additional properties stored in DB
class SubscriptionInDB(SubscriptionInDBBase):
    pass