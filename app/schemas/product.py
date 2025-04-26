from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Shared properties
class ProductBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[float] = None

# Properties to receive via API on creation
class ProductCreate(ProductBase):
    name: str
    user_id: int

# Properties to receive via API on update
class ProductUpdate(ProductBase):
    pass

# Properties shared by models stored in DB
class ProductInDBBase(ProductBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class Product(ProductInDBBase):
    pass

# Additional properties stored in DB
class ProductInDB(ProductInDBBase):
    pass