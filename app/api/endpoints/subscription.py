from typing import Any, Dict, List
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.subscription import Subscription, SubscriptionType
from app.schemas.subscription import (
    Subscription as SubscriptionSchema,
    SubscriptionCreate,
    SubscriptionUpdate,
)

router = APIRouter()

# Mock subscription plans
SUBSCRIPTION_PLANS = [
    {
        "id": 1,
        "name": "Basic Plan",
        "type": SubscriptionType.BASIC,
        "price": 9.99,
        "billing_period": 1,  # monthly
        "features": [
            "Access to AKOOL avatars",
            "Video recording with avatars",
            "Basic customization options",
            "Up to 3 custom avatars",
        ],
    },
    {
        "id": 2,
        "name": "Premium Plan",
        "type": SubscriptionType.PREMIUM,
        "price": 29.99,
        "billing_period": 1,  # monthly
        "features": [
            "Access to all avatars (AKOOL and Soul Machines)",
            "Live interaction with avatars",
            "Advanced customization options",
            "Object recognition and memory features",
            "Up to 10 custom avatars",
            "Priority support",
        ],
    },
    {
        "id": 3,
        "name": "Basic Annual Plan",
        "type": SubscriptionType.BASIC,
        "price": 99.99,
        "billing_period": 12,  # annual
        "features": [
            "Access to AKOOL avatars",
            "Video recording with avatars",
            "Basic customization options",
            "Up to 3 custom avatars",
            "Save 16% compared to monthly",
        ],
    },
    {
        "id": 4,
        "name": "Premium Annual Plan",
        "type": SubscriptionType.PREMIUM,
        "price": 299.99,
        "billing_period": 12,  # annual
        "features": [
            "Access to all avatars (AKOOL and Soul Machines)",
            "Live interaction with avatars",
            "Advanced customization options",
            "Object recognition and memory features",
            "Up to 10 custom avatars",
            "Priority support",
            "Save 16% compared to monthly",
        ],
    },
]

@router.get("/plans", response_model=List[Dict[str, Any]])
def get_subscription_plans(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all available subscription plans.
    """
    return SUBSCRIPTION_PLANS

@router.get("/current", response_model=SubscriptionSchema)
def get_current_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get the current active subscription for the user.
    """
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id, Subscription.is_active == True)
        .first()
    )
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found",
        )
    
    return subscription

@router.get("/history", response_model=List[SubscriptionSchema])
def get_subscription_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get subscription history for the user.
    """
    subscriptions = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id)
        .order_by(Subscription.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return subscriptions

@router.post("/subscribe", response_model=SubscriptionSchema)
def create_subscription(
    *,
    db: Session = Depends(get_db),
    plan_id: int,
    payment_method: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Subscribe to a plan.
    """
    # Find the plan
    plan = next((p for p in SUBSCRIPTION_PLANS if p["id"] == plan_id), None)
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription plan not found",
        )
    
    # Check if user already has an active subscription
    active_subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id, Subscription.is_active == True)
        .first()
    )
    
    if active_subscription:
        # Deactivate the current subscription
        active_subscription.is_active = False
        db.add(active_subscription)
    
    # In a real implementation, we would process the payment here
    # For this example, we'll just create the subscription
    
    # Calculate end date based on billing period
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=30 * plan["billing_period"])
    
    # Create new subscription
    subscription = Subscription(
        type=plan["type"],
        price=plan["price"],
        billing_period=plan["billing_period"],
        is_active=True,
        start_date=start_date,
        end_date=end_date,
        payment_method=payment_method,
        payment_id=f"mock_payment_{datetime.utcnow().timestamp()}",  # Mock payment ID
        user_id=current_user.id,
    )
    
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    
    return subscription

@router.post("/cancel", response_model=Dict[str, Any])
def cancel_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Cancel the current subscription.
    """
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id, Subscription.is_active == True)
        .first()
    )
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found",
        )
    
    # In a real implementation, we would handle the cancellation with the payment provider
    # For this example, we'll just mark the subscription as inactive
    
    subscription.is_active = False
    db.add(subscription)
    db.commit()
    
    return {"success": True, "message": "Subscription cancelled successfully"}