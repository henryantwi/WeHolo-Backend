from sqlalchemy import Boolean, Column, String, Integer, DateTime, ForeignKey, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    image_url = Column(String)
    price = Column(Float)

    # Ownership
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="products")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
