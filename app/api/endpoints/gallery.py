from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.avatar import Avatar
from app.models.subscription import Subscription, SubscriptionType
from app.schemas.avatar import Avatar as AvatarSchema, AvatarCreate

router = APIRouter()

# Mock data for pre-designed avatars (in a real app, this would come from AKOOL API)
PREDESIGNED_AVATARS = [
    {
        "id": 1001,
        "name": "Business Professional",
        "description": "A professional avatar for business presentations and meetings.",
        "image_url": "https://example.com/avatars/business.jpg",
        "provider": "AKOOL",
        "provider_id": "akool-001",
        "is_predesigned": True,
        "is_public": True,
    },
    {
        "id": 1002,
        "name": "Friendly Assistant",
        "description": "A warm and friendly avatar for customer service.",
        "image_url": "https://example.com/avatars/assistant.jpg",
        "provider": "AKOOL",
        "provider_id": "akool-002",
        "is_predesigned": True,
        "is_public": True,
    },
    {
        "id": 1003,
        "name": "Tech Expert",
        "description": "A tech-savvy avatar for explaining complex concepts.",
        "image_url": "https://example.com/avatars/tech.jpg",
        "provider": "AKOOL",
        "provider_id": "akool-003",
        "is_predesigned": True,
        "is_public": True,
    },
    {
        "id": 1004,
        "name": "Medical Professional",
        "description": "A medical avatar for health-related content.",
        "image_url": "https://example.com/avatars/medical.jpg",
        "provider": "SOUL_MACHINES",
        "provider_id": "sm-001",
        "is_predesigned": True,
        "is_public": True,
    },
    {
        "id": 1005,
        "name": "Educational Tutor",
        "description": "An educational avatar for teaching and tutoring.",
        "image_url": "https://example.com/avatars/education.jpg",
        "provider": "SOUL_MACHINES",
        "provider_id": "sm-002",
        "is_predesigned": True,
        "is_public": True,
    },
]

@router.get("/", response_model=List[Dict[str, Any]])
def get_gallery_avatars(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    provider: Optional[str] = None,
) -> Any:
    """
    Get all available avatars for the gallery.
    Optionally filter by provider (AKOOL or SOUL_MACHINES).
    """
    # Get user's active subscription to determine available avatars
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id, Subscription.is_active == True)
        .first()
    )
    
    # Filter avatars based on subscription
    avatars = []
    for avatar in PREDESIGNED_AVATARS:
        # If provider filter is specified, apply it
        if provider and avatar["provider"] != provider:
            continue
            
        # If Soul Machines avatar, check for premium subscription
        if avatar["provider"] == "SOUL_MACHINES":
            if subscription and subscription.type == SubscriptionType.PREMIUM:
                avatars.append(avatar)
        else:
            # AKOOL avatars available to all
            avatars.append(avatar)
    
    return avatars

@router.get("/{avatar_id}", response_model=Dict[str, Any])
def get_gallery_avatar(
    avatar_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific pre-designed avatar by ID.
    """
    # Get user's active subscription to determine available avatars
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id, Subscription.is_active == True)
        .first()
    )
    
    # Find the avatar in the pre-designed list
    avatar = next((a for a in PREDESIGNED_AVATARS if a["id"] == avatar_id), None)
    
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found",
        )
    
    # Check if user has access to this avatar
    if avatar["provider"] == "SOUL_MACHINES" and (not subscription or subscription.type != SubscriptionType.PREMIUM):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required for this avatar",
        )
    
    return avatar

@router.post("/select", response_model=AvatarSchema)
def select_gallery_avatar(
    *,
    db: Session = Depends(get_db),
    avatar_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Select a pre-designed avatar from the gallery and add it to the user's avatars.
    """
    # Get user's active subscription to determine available avatars
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id, Subscription.is_active == True)
        .first()
    )
    
    # Find the avatar in the pre-designed list
    predesigned_avatar = next((a for a in PREDESIGNED_AVATARS if a["id"] == avatar_id), None)
    
    if not predesigned_avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found",
        )
    
    # Check if user has access to this avatar
    if predesigned_avatar["provider"] == "SOUL_MACHINES" and (not subscription or subscription.type != SubscriptionType.PREMIUM):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required for this avatar",
        )
    
    # Check if user already has this avatar
    existing_avatar = (
        db.query(Avatar)
        .filter(
            Avatar.user_id == current_user.id,
            Avatar.provider == predesigned_avatar["provider"],
            Avatar.provider_id == predesigned_avatar["provider_id"],
        )
        .first()
    )
    
    if existing_avatar:
        return existing_avatar
    
    # Create a new avatar for the user based on the pre-designed one
    new_avatar = Avatar(
        name=predesigned_avatar["name"],
        description=predesigned_avatar["description"],
        image_url=predesigned_avatar["image_url"],
        provider=predesigned_avatar["provider"],
        provider_id=predesigned_avatar["provider_id"],
        is_predesigned=True,
        is_public=False,  # User's copy is private by default
        user_id=current_user.id,
    )
    
    db.add(new_avatar)
    db.commit()
    db.refresh(new_avatar)
    
    return new_avatar