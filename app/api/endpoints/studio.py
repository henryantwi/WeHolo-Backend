from typing import Any, Dict, List, Optional
import time

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, DBAPIError, DisconnectionError

from app.api.deps import get_db, get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.avatar import Avatar
from app.models.subscription import Subscription, SubscriptionType
from app.schemas.avatar import Avatar as AvatarSchema, AvatarCreate, AvatarUpdate

router = APIRouter()

@router.get("/avatars", response_model=List[AvatarSchema])
def get_user_avatars(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get all avatars created by the current user.
    """
    avatars = (
        db.query(Avatar)
        .filter(Avatar.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return avatars

@router.post("/avatars", response_model=AvatarSchema)
def create_avatar(
    *,
    db: Session = Depends(get_db),
    avatar_in: AvatarCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new custom avatar.
    """
    try:
        # Check if user has reached their avatar limit
        avatar_count = db.query(Avatar).filter(Avatar.user_id == current_user.id).count()
        
        # Get user's subscription to determine limits
        subscription = (
            db.query(Subscription)
            .filter(Subscription.user_id == current_user.id, Subscription.is_active == True)
            .first()
        )
        
        # Set limits based on subscription
        if subscription and subscription.type == SubscriptionType.PREMIUM:
            max_avatars = 10  # Premium users can have more avatars
        else:
            max_avatars = 3  # Basic users have limited avatars
        
        if avatar_count >= max_avatars:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"You have reached your limit of {max_avatars} avatars. Upgrade your subscription to create more.",
            )
        
        # Create new avatar
        avatar = Avatar(
            name=avatar_in.name,
            description=avatar_in.description,
            image_url=avatar_in.image_url,
            provider=avatar_in.provider,
            provider_id=avatar_in.provider_id,
            behavior_settings={},  # Default empty settings
            appearance_settings={},  # Default empty settings
            voice_settings={},  # Default empty settings
            is_predesigned=False,  # Custom avatar
            is_public=False,  # Private by default
            user_id=current_user.id,
        )
        
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                db.add(avatar)
                db.commit()
                db.refresh(avatar)
                return avatar
            except (OperationalError, DBAPIError, DisconnectionError) as e:
                if attempt < max_retries - 1:
                    db.rollback()  # Important: rollback the transaction
                    time.sleep(retry_delay)
                    continue
                else:
                    # If all retries fail, raise a user-friendly error
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Database connection error, please try again",
                    ) from e
    except Exception as e:
        # Catch any other unexpected errors
        db.rollback()
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create avatar. Please try again.",
        ) from e

@router.get("/avatars/{avatar_id}", response_model=AvatarSchema)
def get_avatar(
    avatar_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific avatar by ID.
    """
    avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()
    
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found",
        )
    
    # Check if user owns this avatar
    if avatar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this avatar",
        )
    
    return avatar

@router.put("/avatars/{avatar_id}", response_model=AvatarSchema)
def update_avatar(
    *,
    avatar_id: int,
    db: Session = Depends(get_db),
    avatar_in: AvatarUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update an avatar.
    """
    avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()
    
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found",
        )
    
    # Check if user owns this avatar
    if avatar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify this avatar",
        )
    
    # Update avatar attributes
    if avatar_in.name is not None:
        avatar.name = avatar_in.name
    
    if avatar_in.description is not None:
        avatar.description = avatar_in.description
    
    if avatar_in.image_url is not None:
        avatar.image_url = avatar_in.image_url
    
    if avatar_in.behavior_settings is not None:
        avatar.behavior_settings = avatar_in.behavior_settings
    
    if avatar_in.appearance_settings is not None:
        avatar.appearance_settings = avatar_in.appearance_settings
    
    if avatar_in.voice_settings is not None:
        avatar.voice_settings = avatar_in.voice_settings
    
    if avatar_in.is_public is not None:
        avatar.is_public = avatar_in.is_public
    
    db.add(avatar)
    db.commit()
    db.refresh(avatar)
    
    return avatar

@router.delete("/avatars/{avatar_id}", response_model=Dict[str, Any])
def delete_avatar(
    avatar_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete an avatar.
    """
    avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()
    
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found",
        )
    
    # Check if user owns this avatar
    if avatar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this avatar",
        )
    
    db.delete(avatar)
    db.commit()
    
    return {"success": True, "message": "Avatar deleted successfully"}

@router.post("/upload-photo", response_model=Dict[str, Any])
async def upload_photo_for_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload a photo to create a custom avatar.
    In a real implementation, this would integrate with AKOOL API to create a custom avatar.
    """
    # Check if user has an active subscription
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id, Subscription.is_active == True)
        .first()
    )
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Subscription required to create custom avatars from photos",
        )
    
    # In a real implementation, we would:
    # 1. Save the uploaded file
    # 2. Call the AKOOL API to create a custom avatar
    # 3. Store the avatar details in the database
    
    # For this example, we'll just return a mock response
    return {
        "success": True,
        "message": "Photo uploaded successfully. Avatar creation in progress.",
        "estimated_time": "5 minutes",
    }