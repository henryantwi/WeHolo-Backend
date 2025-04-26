from sqlalchemy import Boolean, Column, String, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base

class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    is_user = Column(Boolean, default=True)  # True if message is from user, False if from avatar

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    conversation_id = Column(Integer, ForeignKey("conversation.id"))
    conversation = relationship("Conversation", back_populates="messages")

class Conversation(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

    # Relationships
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="conversations")

    avatar_id = Column(Integer, ForeignKey("avatar.id"))
    avatar = relationship("Avatar", back_populates="conversations")

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Metadata
    conversation_metadata = Column(JSON)  # For storing additional information about the conversation
