from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.avatar import Avatar
from app.models.subscription import Subscription, SubscriptionType
from app.models.conversation import Conversation
from app.schemas.avatar import Avatar as AvatarSchema
from app.schemas.subscription import Subscription as SubscriptionSchema
from app.schemas.conversation import Conversation as ConversationSchema

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get dashboard data for the current user.
    """
    # Get user's avatars
    avatars = db.query(Avatar).filter(Avatar.user_id == current_user.id).all()
    
    # Get user's active subscription
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id, Subscription.is_active == True)
        .first()
    )
    
    # Get user's recent conversations
    recent_conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
        .limit(5)
        .all()
    )
    
    # Determine available features based on subscription
    available_features = {
        "avatar_creation": True,  # Basic feature available to all
        "avatar_customization": True,  # Basic feature available to all
        "video_recording": subscription is not None,  # Requires any subscription
        "live_interaction": subscription is not None and subscription.type == SubscriptionType.PREMIUM,  # Requires premium
        "object_recognition": subscription is not None and subscription.type == SubscriptionType.PREMIUM,  # Requires premium
        "memory": subscription is not None and subscription.type == SubscriptionType.PREMIUM,  # Requires premium
    }
    
    return {
        "user_preferences": {
            "language": current_user.language,
            "ui_theme": current_user.ui_theme,
            "camera_mode": current_user.camera_mode,
        },
        "avatars": avatars,
        "subscription": subscription,
        "recent_conversations": recent_conversations,
        "available_features": available_features,
    }

@router.put("/preferences", response_model=Dict[str, Any])
def update_preferences(
    *,
    db: Session = Depends(get_db),
    preferences: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update user preferences.
    """
    # Query the user from the database to ensure we're working with a session-bound instance
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if "language" in preferences:
        user.language = preferences["language"]
    
    if "ui_theme" in preferences:
        user.ui_theme = preferences["ui_theme"]
    
    if "camera_mode" in preferences:
        user.camera_mode = preferences["camera_mode"]
    
    db.commit()
    db.refresh(user)
    
    return {
        "language": user.language,
        "ui_theme": user.ui_theme,
        "camera_mode": user.camera_mode,
    }