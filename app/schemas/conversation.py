from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

# Message schemas
class MessageBase(BaseModel):
    content: str
    is_user: Optional[bool] = True

# Properties to receive via API on creation
class MessageCreate(MessageBase):
    conversation_id: int

# Properties to receive via API on update
class MessageUpdate(MessageBase):
    pass

# Properties shared by models stored in DB
class MessageInDBBase(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Additional properties to return via API
class Message(MessageInDBBase):
    pass

# Additional properties stored in DB
class MessageInDB(MessageInDBBase):
    pass

# Conversation schemas
class ConversationBase(BaseModel):
    title: Optional[str] = None
    conversation_metadata: Optional[Dict[str, Any]] = None

# Properties to receive via API on creation
class ConversationCreate(ConversationBase):
    user_id: int
    avatar_id: int

# Properties to receive via API on update
class ConversationUpdate(ConversationBase):
    pass

# Properties shared by models stored in DB
class ConversationInDBBase(ConversationBase):
    id: int
    user_id: int
    avatar_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class Conversation(ConversationInDBBase):
    pass

# Additional properties to return via API with messages
class ConversationWithMessages(Conversation):
    messages: List[Message] = []

# Additional properties stored in DB
class ConversationInDB(ConversationInDBBase):
    pass
