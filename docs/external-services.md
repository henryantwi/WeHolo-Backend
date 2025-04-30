# External Services Integration

This document provides information about the external services that WeHolo integrates with and how to use them in your development.

## Overview

WeHolo integrates with two primary external services for avatar functionality:

1. **AKOOL API**: Used for basic avatar creation and customization
2. **Soul Machines API**: Used for premium avatar experiences with advanced interaction capabilities

## AKOOL API

AKOOL provides a platform for creating and customizing 3D avatars with basic animation capabilities.

### Authentication

To use the AKOOL API, you need an API key. This key should be set in your environment variables:

```
AKOOL_API_KEY=your-akool-api-key
```

### Endpoints

The AKOOL API is accessed through the following base URL:

```
https://api.akool.com/v1
```

### Key Features

- **Avatar Gallery**: Browse pre-designed avatars
- **Avatar Customization**: Modify avatar appearance
- **Video Generation**: Generate videos with avatar animations

### Implementation

The AKOOL API integration is implemented in `app/services/akool.py`. Here's a simplified example of how to use it:

```python
import os
import requests
from app.core.config import settings

class AkoolService:
    def __init__(self):
        self.api_key = settings.AKOOL_API_KEY
        self.base_url = "https://api.akool.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_avatars(self, limit=10, offset=0):
        """
        Retrieve available avatars from AKOOL
        """
        url = f"{self.base_url}/avatars"
        params = {"limit": limit, "offset": offset}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def create_video(self, avatar_id, text, options=None):
        """
        Generate a video with the specified avatar speaking the text
        """
        url = f"{self.base_url}/videos"
        
        data = {
            "avatar_id": avatar_id,
            "text": text,
            "options": options or {}
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        
        return response.json()
```

### Rate Limits

The AKOOL API has the following rate limits:

- 100 requests per minute
- 1,000 requests per day for the basic tier
- 10,000 requests per day for the premium tier

### Error Handling

Handle AKOOL API errors with appropriate error codes:

```python
try:
    avatars = akool_service.get_avatars()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        # Handle authentication error
        logger.error("Invalid AKOOL API key")
    elif e.response.status_code == 429:
        # Handle rate limit error
        logger.error("AKOOL API rate limit exceeded")
    else:
        # Handle other errors
        logger.error(f"AKOOL API error: {str(e)}")
```

## Soul Machines API

Soul Machines provides more advanced avatar experiences with realistic facial expressions and real-time interaction capabilities.

### Authentication

To use the Soul Machines API, you need an API key. This key should be set in your environment variables:

```
SOUL_MACHINES_API_KEY=your-soul-machines-api-key
```

### Endpoints

The Soul Machines API is accessed through the following base URL:

```
https://api.soulmachines.com/v1
```

### Key Features

- **Digital People**: Highly realistic avatars with natural expressions
- **Real-time Interaction**: Live conversation capabilities
- **Emotion Recognition**: Avatars can respond to user emotions
- **Multi-modal Interaction**: Support for text, voice, and video input

### Implementation

The Soul Machines API integration is implemented in `app/services/soul_machines.py`. Here's a simplified example of how to use it:

```python
import os
import requests
from app.core.config import settings

class SoulMachinesService:
    def __init__(self):
        self.api_key = settings.SOUL_MACHINES_API_KEY
        self.base_url = "https://api.soulmachines.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_digital_people(self, limit=10, offset=0):
        """
        Retrieve available digital people from Soul Machines
        """
        url = f"{self.base_url}/digital-people"
        params = {"limit": limit, "offset": offset}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def create_conversation(self, digital_person_id):
        """
        Create a new conversation with a digital person
        """
        url = f"{self.base_url}/conversations"
        
        data = {
            "digital_person_id": digital_person_id
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        
        return response.json()
    
    def send_message(self, conversation_id, message):
        """
        Send a message to a digital person in a conversation
        """
        url = f"{self.base_url}/conversations/{conversation_id}/messages"
        
        data = {
            "content": message,
            "type": "text"
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        
        return response.json()
```

### WebSocket Integration

For real-time interaction, Soul Machines provides a WebSocket API:

```python
import websocket
import json
import threading

class SoulMachinesWebSocket:
    def __init__(self, conversation_id, api_key, on_message=None):
        self.conversation_id = conversation_id
        self.api_key = api_key
        self.on_message = on_message or (lambda msg: print(f"Received: {msg}"))
        self.ws = None
        self.thread = None
    
    def connect(self):
        """
        Connect to the Soul Machines WebSocket API
        """
        url = f"wss://api.soulmachines.com/v1/conversations/{self.conversation_id}/ws"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        self.ws = websocket.WebSocketApp(
            url,
            header=headers,
            on_message=lambda ws, msg: self.on_message(json.loads(msg)),
            on_error=lambda ws, err: print(f"Error: {err}"),
            on_close=lambda ws, close_status_code, close_msg: print("Connection closed")
        )
        
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()
    
    def send(self, message):
        """
        Send a message through the WebSocket
        """
        if self.ws:
            self.ws.send(json.dumps({
                "type": "text",
                "content": message
            }))
    
    def close(self):
        """
        Close the WebSocket connection
        """
        if self.ws:
            self.ws.close()
            self.thread.join(timeout=1)
```

### Rate Limits

The Soul Machines API has the following rate limits:

- 60 requests per minute
- 500 requests per day for the basic tier
- 5,000 requests per day for the premium tier

### Error Handling

Handle Soul Machines API errors with appropriate error codes:

```python
try:
    digital_people = soul_machines_service.get_digital_people()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        # Handle authentication error
        logger.error("Invalid Soul Machines API key")
    elif e.response.status_code == 429:
        # Handle rate limit error
        logger.error("Soul Machines API rate limit exceeded")
    else:
        # Handle other errors
        logger.error(f"Soul Machines API error: {str(e)}")
```

## Subscription Tiers

WeHolo offers different subscription tiers that determine which avatar services are available to users:

1. **Basic Tier**: Access to AKOOL avatars only
2. **Premium Tier**: Access to both AKOOL and Soul Machines avatars

The subscription tier is checked in the API endpoints before making requests to the external services:

```python
@router.get("/avatars")
def get_avatars(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check user's subscription tier
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.is_active == True
    ).first()
    
    # Get avatars based on subscription tier
    if subscription and subscription.type == SubscriptionType.PREMIUM:
        # Premium user - get avatars from both services
        akool_avatars = akool_service.get_avatars()
        soul_machines_avatars = soul_machines_service.get_digital_people()
        return {
            "akool_avatars": akool_avatars,
            "soul_machines_avatars": soul_machines_avatars
        }
    else:
        # Basic user - get avatars from AKOOL only
        akool_avatars = akool_service.get_avatars()
        return {
            "akool_avatars": akool_avatars,
            "soul_machines_avatars": []
        }
```

## Caching

To reduce API calls and improve performance, WeHolo implements caching for external service responses:

```python
from functools import lru_cache

class CachedAkoolService(AkoolService):
    @lru_cache(maxsize=100)
    def get_avatars(self, limit=10, offset=0):
        """
        Cached version of get_avatars
        """
        return super().get_avatars(limit, offset)
```

## Testing with Mock Services

For testing purposes, mock implementations of the external services are provided:

```python
class MockAkoolService(AkoolService):
    def get_avatars(self, limit=10, offset=0):
        """
        Mock implementation that returns test data
        """
        return [
            {
                "id": "avatar1",
                "name": "Test Avatar 1",
                "thumbnail_url": "https://example.com/avatar1.jpg"
            },
            {
                "id": "avatar2",
                "name": "Test Avatar 2",
                "thumbnail_url": "https://example.com/avatar2.jpg"
            }
        ][:limit]
    
    def create_video(self, avatar_id, text, options=None):
        """
        Mock implementation that returns test data
        """
        return {
            "id": "video1",
            "status": "processing",
            "url": None,
            "estimated_completion_time": 30
        }
```

## Troubleshooting

### Common Issues

1. **API Key Issues**
   - Ensure your API keys are correctly set in the environment variables
   - Verify that your API keys are valid and not expired
   - Check that you have the correct permissions for the API endpoints you're accessing

2. **Rate Limiting**
   - Implement exponential backoff for retries
   - Consider caching responses to reduce API calls
   - Monitor your API usage to stay within limits

3. **Network Issues**
   - Implement proper timeout handling
   - Add retry logic for transient network failures
   - Log detailed error information for debugging

### Getting Help

If you encounter issues with the external services:

- Check the service's documentation and status page
- Contact the service's support team
- Look for community forums or discussion groups