from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.avatar import Avatar
from app.models.conversation import Conversation, Message
from app.models.product import Product
from app.models.subscription import Subscription, SubscriptionType
from app.schemas.conversation import (
    Conversation as ConversationSchema,
    ConversationCreate,
    ConversationWithMessages,
    Message as MessageSchema,
    MessageCreate,
)

router = APIRouter()

@router.get("/conversations", response_model=List[ConversationSchema])
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get all conversations for the current user.
    """
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return conversations

@router.post("/conversations", response_model=ConversationSchema)
def create_conversation(
    *,
    db: Session = Depends(get_db),
    conversation_in: ConversationCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new conversation.
    """
    # Check if the avatar exists and belongs to the user
    avatar = db.query(Avatar).filter(Avatar.id == conversation_in.avatar_id).first()
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found",
        )

    if avatar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to use this avatar",
        )

    # Create new conversation
    conversation = Conversation(
        title=conversation_in.title or f"Conversation with {avatar.name}",
        user_id=current_user.id,
        avatar_id=avatar.id,
        conversation_metadata=conversation_in.conversation_metadata or {},
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation

@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific conversation by ID with all messages.
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    # Check if user owns this conversation
    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this conversation",
        )

    # Get all messages for this conversation
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
        .all()
    )

    # Create response with conversation and messages
    result = ConversationWithMessages.model_validate(conversation)
    result.messages = messages

    return result

@router.post("/conversations/{conversation_id}/messages", response_model=MessageSchema)
def create_message(
    *,
    conversation_id: int,
    db: Session = Depends(get_db),
    message_in: MessageCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Add a new message to a conversation.
    """
    # Check if conversation exists and belongs to the user
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this conversation",
        )

    # Create user message
    user_message = Message(
        content=message_in.content,
        is_user=True,
        conversation_id=conversation.id,
    )

    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Get the avatar for this conversation
    avatar = db.query(Avatar).filter(Avatar.id == conversation.avatar_id).first()

    # In a real implementation, we would call the appropriate API (AKOOL or Soul Machines)
    # to generate a response from the avatar. For this example, we'll create a mock response.

    # Check if any products are mentioned in the message
    products = db.query(Product).filter(Product.user_id == current_user.id).all()
    mentioned_product = None

    for product in products:
        if product.name.lower() in message_in.content.lower():
            mentioned_product = product
            break

    # Generate avatar response
    response_content = f"I received your message: '{message_in.content}'. "

    if mentioned_product:
        response_content += f"I see you mentioned {mentioned_product.name}. "
        if mentioned_product.description:
            response_content += f"Here's some information about it: {mentioned_product.description}"
    else:
        response_content += "How can I assist you further?"

    # Create avatar response message
    avatar_message = Message(
        content=response_content,
        is_user=False,
        conversation_id=conversation.id,
    )

    db.add(avatar_message)

    # Update conversation's updated_at timestamp
    conversation.updated_at = db.func.now()
    db.add(conversation)

    db.commit()
    db.refresh(avatar_message)

    return avatar_message

@router.delete("/conversations/{conversation_id}", response_model=Dict[str, Any])
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a conversation.
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    # Check if user owns this conversation
    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this conversation",
        )

    # Delete all messages in the conversation
    db.query(Message).filter(Message.conversation_id == conversation.id).delete()

    # Delete the conversation
    db.delete(conversation)
    db.commit()

    return {"success": True, "message": "Conversation deleted successfully"}

# WebSocket endpoint for real-time chat
# Note: This is a simplified implementation. In a real application,
# you would need to handle authentication, manage connections, etc.
@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    conversation_id: int,
    db: Session = Depends(get_db),
):
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            # In a real implementation, you would:
            # 1. Verify the user has access to this conversation
            # 2. Save the message to the database
            # 3. Process the message (e.g., send to AKOOL or Soul Machines API)
            # 4. Generate and save the response
            # 5. Send the response back to the client

            # For this example, we'll just echo the message back
            await websocket.send_text(f"You said: {data}")

            # Send a mock avatar response
            await websocket.send_text(f"Avatar response: I received your message '{data}'")
    except WebSocketDisconnect:
        # Handle disconnect
        pass
