from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.subscription import Subscription, SubscriptionType

router = APIRouter()

# Mock data for demo videos
DEMO_VIDEOS = [
    {
        "id": 1,
        "title": "Business Presentation",
        "description": "Demonstration of an avatar giving a business presentation.",
        "video_url": "https://example.com/demos/business.mp4",
        "thumbnail_url": "https://example.com/demos/business_thumb.jpg",
        "avatar_provider": "AKOOL",
        "duration": 120,  # seconds
        "features": ["lip_sync", "gestures", "emotions"],
    },
    {
        "id": 2,
        "title": "Customer Service",
        "description": "Demonstration of an avatar handling customer service inquiries.",
        "video_url": "https://example.com/demos/customer_service.mp4",
        "thumbnail_url": "https://example.com/demos/customer_service_thumb.jpg",
        "avatar_provider": "AKOOL",
        "duration": 180,  # seconds
        "features": ["lip_sync", "gestures", "emotions"],
    },
    {
        "id": 3,
        "title": "Educational Content",
        "description": "Demonstration of an avatar teaching a complex topic.",
        "video_url": "https://example.com/demos/education.mp4",
        "thumbnail_url": "https://example.com/demos/education_thumb.jpg",
        "avatar_provider": "AKOOL",
        "duration": 240,  # seconds
        "features": ["lip_sync", "gestures", "emotions"],
    },
    {
        "id": 4,
        "title": "Interactive Medical Consultation",
        "description": "Demonstration of an avatar providing medical information and responding to questions.",
        "video_url": "https://example.com/demos/medical.mp4",
        "thumbnail_url": "https://example.com/demos/medical_thumb.jpg",
        "avatar_provider": "SOUL_MACHINES",
        "duration": 300,  # seconds
        "features": ["lip_sync", "gestures", "emotions", "object_recognition", "memory"],
    },
    {
        "id": 5,
        "title": "Real-time Customer Support",
        "description": "Demonstration of an avatar providing real-time support with natural interactions.",
        "video_url": "https://example.com/demos/support.mp4",
        "thumbnail_url": "https://example.com/demos/support_thumb.jpg",
        "avatar_provider": "SOUL_MACHINES",
        "duration": 270,  # seconds
        "features": ["lip_sync", "gestures", "emotions", "object_recognition", "memory"],
    },
]

@router.get("/", response_model=List[Dict[str, Any]])
def get_demo_videos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all available demo videos.
    """
    # Get user's active subscription to determine available demos
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id, Subscription.is_active == True)
        .first()
    )
    
    # Filter demos based on subscription
    demos = []
    for demo in DEMO_VIDEOS:
        # If Soul Machines demo, check for premium subscription
        if demo["avatar_provider"] == "SOUL_MACHINES":
            if subscription and subscription.type == SubscriptionType.PREMIUM:
                demos.append(demo)
        else:
            # AKOOL demos available to all
            demos.append(demo)
    
    return demos

@router.get("/{demo_id}", response_model=Dict[str, Any])
def get_demo_video(
    demo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific demo video by ID.
    """
    # Get user's active subscription to determine available demos
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id, Subscription.is_active == True)
        .first()
    )
    
    # Find the demo in the list
    demo = next((d for d in DEMO_VIDEOS if d["id"] == demo_id), None)
    
    if not demo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demo video not found",
        )
    
    # Check if user has access to this demo
    if demo["avatar_provider"] == "SOUL_MACHINES" and (not subscription or subscription.type != SubscriptionType.PREMIUM):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required for this demo",
        )
    
    return demo