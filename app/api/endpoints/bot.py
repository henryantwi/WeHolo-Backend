from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.avatar import Avatar
from app.models.subscription import Subscription, SubscriptionType

router = APIRouter()

# Mock data for avatar recommendations based on user preferences
AVATAR_RECOMMENDATIONS = {
    "business": [
        {
            "id": 1001,  # This ID matches the one in gallery.py
            "name": "Business Professional",
            "description": "A professional avatar for business presentations and meetings.",
            "image_url": "https://example.com/avatars/business.jpg",
            "provider": "AKOOL",
            "provider_id": "akool-001",
            "reason": "Perfect for business presentations and professional meetings.",
        },
    ],
    "customer_service": [
        {
            "id": 1002,  # This ID matches the one in gallery.py
            "name": "Friendly Assistant",
            "description": "A warm and friendly avatar for customer service.",
            "image_url": "https://example.com/avatars/assistant.jpg",
            "provider": "AKOOL",
            "provider_id": "akool-002",
            "reason": "Designed to provide friendly and helpful customer service interactions.",
        },
    ],
    "education": [
        {
            "id": 1003,  # This ID matches the one in gallery.py
            "name": "Tech Expert",
            "description": "A tech-savvy avatar for explaining complex concepts.",
            "image_url": "https://example.com/avatars/tech.jpg",
            "provider": "AKOOL",
            "provider_id": "akool-003",
            "reason": "Great for explaining technical concepts in an easy-to-understand way.",
        },
        {
            "id": 1005,  # This ID matches the one in gallery.py
            "name": "Educational Tutor",
            "description": "An educational avatar for teaching and tutoring.",
            "image_url": "https://example.com/avatars/education.jpg",
            "provider": "SOUL_MACHINES",
            "provider_id": "sm-002",
            "reason": "Specialized in educational content and interactive learning experiences.",
        },
    ],
    "healthcare": [
        {
            "id": 1004,  # This ID matches the one in gallery.py
            "name": "Medical Professional",
            "description": "A medical avatar for health-related content.",
            "image_url": "https://example.com/avatars/medical.jpg",
            "provider": "SOUL_MACHINES",
            "provider_id": "sm-001",
            "reason": "Designed for healthcare-related content and medical information.",
        },
    ],
}

@router.post("/recommend", response_model=List[Dict[str, Any]])
def recommend_avatars(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    user_input: Dict[str, Any],
) -> Any:
    """
    Recommend avatars based on user input.
    The user can describe what they're looking for, and the bot will recommend avatars.
    """
    # Get user's active subscription to determine available avatars
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id, Subscription.is_active == True)
        .first()
    )
    
    # Extract keywords from user input
    input_text = user_input.get("text", "").lower()
    
    # Simple keyword matching for categories
    categories = []
    if any(word in input_text for word in ["business", "professional", "corporate", "presentation", "meeting"]):
        categories.append("business")
    
    if any(word in input_text for word in ["customer", "service", "support", "help", "assistant"]):
        categories.append("customer_service")
    
    if any(word in input_text for word in ["education", "teach", "learn", "tutor", "school", "university", "student"]):
        categories.append("education")
    
    if any(word in input_text for word in ["health", "medical", "doctor", "nurse", "patient", "hospital", "clinic"]):
        categories.append("healthcare")
    
    # If no categories matched, provide a general recommendation
    if not categories:
        categories = ["business", "customer_service"]  # Default categories
    
    # Collect recommendations from matched categories
    recommendations = []
    for category in categories:
        if category in AVATAR_RECOMMENDATIONS:
            for avatar in AVATAR_RECOMMENDATIONS[category]:
                # Filter out Soul Machines avatars if user doesn't have premium subscription
                if avatar["provider"] == "SOUL_MACHINES" and (not subscription or subscription.type != SubscriptionType.PREMIUM):
                    continue
                
                # Check if this avatar is already in recommendations
                if not any(r["id"] == avatar["id"] for r in recommendations):
                    recommendations.append(avatar)
    
    return recommendations

@router.post("/chat", response_model=Dict[str, Any])
def chat_with_bot(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    message: Dict[str, str],
) -> Any:
    """
    Chat with the beginner-friendly bot.
    The bot can help users understand how to use the platform and recommend avatars.
    """
    user_message = message.get("text", "")
    
    # Simple rule-based responses
    if any(word in user_message.lower() for word in ["hello", "hi", "hey", "greetings"]):
        return {
            "message": "Hello! I'm your WeHolo assistant. I can help you find the perfect avatar for your needs. What kind of avatar are you looking for?",
            "suggestions": ["Business avatar", "Customer service avatar", "Educational avatar", "Healthcare avatar"]
        }
    
    elif any(word in user_message.lower() for word in ["avatar", "recommend", "suggestion"]):
        return {
            "message": "I'd be happy to recommend an avatar for you! Could you tell me what you'll be using it for? For example, business presentations, customer service, education, or healthcare?",
            "suggestions": ["Business presentations", "Customer service", "Education", "Healthcare"]
        }
    
    elif any(word in user_message.lower() for word in ["business", "presentation", "meeting", "corporate"]):
        return {
            "message": "For business presentations, I recommend the 'Business Professional' avatar. It's designed to deliver professional presentations with clear communication and appropriate gestures.",
            "suggestions": ["Show me this avatar", "What other avatars do you have?", "How do I customize it?"]
        }
    
    elif any(word in user_message.lower() for word in ["customer", "service", "support", "help"]):
        return {
            "message": "For customer service, the 'Friendly Assistant' avatar is a great choice. It's warm, approachable, and designed to make customers feel comfortable.",
            "suggestions": ["Show me this avatar", "What other avatars do you have?", "How do I customize it?"]
        }
    
    elif any(word in user_message.lower() for word in ["education", "teach", "learn", "tutor"]):
        return {
            "message": "For educational content, I recommend either the 'Tech Expert' for technical subjects or the 'Educational Tutor' for general education. The Educational Tutor requires a premium subscription.",
            "suggestions": ["Show me these avatars", "Tell me about premium features", "How do I subscribe?"]
        }
    
    elif any(word in user_message.lower() for word in ["health", "medical", "doctor", "healthcare"]):
        return {
            "message": "For healthcare content, the 'Medical Professional' avatar is ideal. It's designed to communicate medical information clearly and professionally. This avatar requires a premium subscription.",
            "suggestions": ["Tell me about premium features", "How do I subscribe?", "Show me other avatars"]
        }
    
    elif any(word in user_message.lower() for word in ["subscription", "premium", "plan", "price", "cost"]):
        return {
            "message": "We offer two subscription tiers: Basic and Premium. Basic gives you access to AKOOL avatars, while Premium adds Soul Machines avatars with advanced features like object recognition and memory. You can view all plans in the Subscription section.",
            "suggestions": ["Show me subscription plans", "What's included in Premium?", "How do I upgrade?"]
        }
    
    elif any(word in user_message.lower() for word in ["customize", "edit", "modify", "change"]):
        return {
            "message": "You can customize your avatars in the Studio section. There, you can adjust their appearance, behavior, voice, and more. Different avatars have different customization options.",
            "suggestions": ["Take me to Studio", "What can I customize?", "Show me examples"]
        }
    
    elif any(word in user_message.lower() for word in ["help", "how", "guide", "tutorial"]):
        return {
            "message": "I'm here to help! You can explore avatars in the Gallery, customize them in the Studio, and manage your subscription in the Subscription section. What would you like to know more about?",
            "suggestions": ["How to create an avatar", "How to start a conversation", "How to add products"]
        }
    
    else:
        return {
            "message": "I'm not sure I understand. Could you tell me more about what you're looking for? I can help with finding avatars, customizing them, or understanding subscription plans.",
            "suggestions": ["Recommend an avatar", "Tell me about subscriptions", "How to use the platform"]
        }