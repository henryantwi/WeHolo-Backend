from sqlalchemy import Boolean, Column, String, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base

class Avatar(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    image_url = Column(String)

    # Avatar type (AKOOL or Soul Machines)
    provider = Column(String, nullable=False)
    provider_id = Column(String)  # ID in the provider's system

    # Avatar behavior settings
    behavior_settings = Column(JSON)

    # Avatar customization
    appearance_settings = Column(JSON)
    voice_settings = Column(JSON)

    # Ownership
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="avatars")

    # Conversations
    conversations = relationship("Conversation", back_populates="avatar", cascade="all, delete-orphan")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Is this a pre-designed avatar?
    is_predesigned = Column(Boolean, default=False)

    # Is this avatar public?
    is_public = Column(Boolean, default=False)
