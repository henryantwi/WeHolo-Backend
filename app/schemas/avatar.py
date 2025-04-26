from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field

# Shared properties
class AvatarBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    provider: Optional[str] = None
    provider_id: Optional[str] = None
    behavior_settings: Optional[Dict[str, Any]] = None
    appearance_settings: Optional[Dict[str, Any]] = None
    voice_settings: Optional[Dict[str, Any]] = None
    is_predesigned: Optional[bool] = False
    is_public: Optional[bool] = False

# Properties to receive via API on creation
class AvatarCreate(AvatarBase):
    name: str
    provider: str
    user_id: int

# Properties to receive via API on update
class AvatarUpdate(AvatarBase):
    pass

# Properties shared by models stored in DB
class AvatarInDBBase(AvatarBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class Avatar(AvatarInDBBase):
    pass

# Additional properties stored in DB
class AvatarInDB(AvatarInDBBase):
    pass