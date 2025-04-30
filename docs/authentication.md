# Authentication and Authorization

This document describes the authentication and authorization system used in the WeHolo platform.

## Overview

WeHolo uses JSON Web Tokens (JWT) for authentication. This stateless authentication mechanism allows the API to scale horizontally without shared session storage.

## Authentication Flow

1. User submits credentials (email and password) to the `/api/auth/login` endpoint
2. The server validates the credentials against the database
3. If valid, the server generates a JWT token and returns it to the client
4. For subsequent requests, the client includes the token in the `Authorization` header
5. The server validates the token and identifies the user for each request

## JWT Tokens

### Token Structure

JWT tokens consist of three parts:
- **Header**: Contains the token type and signing algorithm
- **Payload**: Contains claims about the user (e.g., user ID, expiration time)
- **Signature**: Ensures the token hasn't been tampered with

### Token Claims

The JWT payload contains the following claims:
- `sub`: Subject (user ID)
- `exp`: Expiration time

### Token Expiration

By default, tokens expire after 8 days (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` environment variable).

## Authentication Endpoints

### Login

**URL:** `/api/auth/login`

**Method:** `POST`

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "userpassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Test Token

**URL:** `/api/auth/test-token`

**Method:** `POST`

**Authentication Required:** Yes

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false
}
```

## Password Handling

Passwords are never stored in plain text. Instead, they are hashed using bcrypt, a secure one-way hashing algorithm.

### Password Hashing

When a user is created or changes their password:
1. The plain text password is hashed using bcrypt
2. Only the hash is stored in the database

### Password Verification

When a user attempts to log in:
1. The submitted password is hashed using the same algorithm
2. The resulting hash is compared with the stored hash
3. If they match, the password is correct

## Authorization

WeHolo implements role-based access control to restrict access to certain endpoints.

### User Roles

- **Regular User**: Standard user with access to their own resources
- **Superuser**: Administrative user with access to all resources

### Permission Checks

Permission checks are implemented using FastAPI dependencies:

- `get_current_user`: Ensures the request is authenticated
- `get_current_active_user`: Ensures the authenticated user is active
- `get_current_active_superuser`: Ensures the authenticated user is an active superuser

## Implementation

The authentication system is implemented in the following files:

- `app/core/security.py`: Contains functions for token creation, password hashing, and user authentication
- `app/api/deps.py`: Contains dependencies for authentication and authorization
- `app/api/endpoints/auth.py`: Contains the authentication endpoints

## Security Considerations

### Token Storage

Clients should store tokens securely:
- Web applications: HttpOnly cookies or secure local storage
- Mobile applications: Secure storage mechanisms provided by the platform

### HTTPS

All API requests should be made over HTTPS to prevent token interception.

### Token Refresh

For enhanced security, implement token refresh:
1. Issue short-lived access tokens and longer-lived refresh tokens
2. When the access token expires, use the refresh token to obtain a new access token
3. If the refresh token is compromised, it can be revoked

## Example Usage

### Authenticating a User

```python
import requests

# Login and get token
response = requests.post(
    "https://api.weholo.com/api/auth/login",
    json={"username": "user@example.com", "password": "userpassword"}
)
token = response.json()["access_token"]

# Use token for authenticated requests
headers = {"Authorization": f"Bearer {token}"}
user_response = requests.get(
    "https://api.weholo.com/api/users/me",
    headers=headers
)
user_data = user_response.json()
```

### Implementing a Protected Endpoint

```python
from fastapi import APIRouter, Depends
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_active_user)):
    return {"message": f"Hello, {current_user.full_name}!"}
```

## Troubleshooting

### Invalid Token

If you receive a 401 Unauthorized error with the message "Could not validate credentials", check:
1. The token is included in the Authorization header with the "Bearer" prefix
2. The token is valid and hasn't expired
3. The token was issued by the same server you're making the request to

### Insufficient Permissions

If you receive a 403 Forbidden error with the message "The user doesn't have enough privileges", check:
1. The authenticated user has the required role (e.g., superuser)
2. The authenticated user is active