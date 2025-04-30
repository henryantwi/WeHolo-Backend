# Users API

The Users API provides endpoints for managing user accounts and profiles.

## Endpoints

### Get Current User

Retrieves the profile of the currently authenticated user.

**URL:** `/api/users/me`

**Method:** `GET`

**Authentication Required:** Yes

**Permissions Required:** Active user

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z",
  "language": "en",
  "ui_theme": "light",
  "camera_mode": "standard"
}
```

### Update Current User

Updates the profile of the currently authenticated user.

**URL:** `/api/users/me`

**Method:** `PUT`

**Authentication Required:** Yes

**Permissions Required:** Active user

**Request Body:**

```json
{
  "email": "newemail@example.com",
  "full_name": "New Name",
  "password": "newpassword",
  "language": "fr",
  "ui_theme": "dark",
  "camera_mode": "cinematic"
}
```

All fields are optional. Only the fields that are provided will be updated.

**Response:**

```json
{
  "id": 1,
  "email": "newemail@example.com",
  "full_name": "New Name",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-03T00:00:00Z",
  "language": "fr",
  "ui_theme": "dark",
  "camera_mode": "cinematic"
}
```

### Get User by ID

Retrieves a specific user by their ID.

**URL:** `/api/users/{user_id}`

**Method:** `GET`

**Authentication Required:** Yes

**Permissions Required:** 
- Active user (can only retrieve their own profile)
- Superuser (can retrieve any user profile)

**Path Parameters:**
- `user_id` (integer): The ID of the user to retrieve

**Response:**

```json
{
  "id": 2,
  "email": "another@example.com",
  "full_name": "Another User",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z",
  "language": "en",
  "ui_theme": "light",
  "camera_mode": "standard"
}
```

### List Users

Retrieves a list of all users.

**URL:** `/api/users/`

**Method:** `GET`

**Authentication Required:** Yes

**Permissions Required:** Superuser

**Query Parameters:**
- `skip` (integer, optional): Number of users to skip (default: 0)
- `limit` (integer, optional): Maximum number of users to return (default: 100)

**Response:**

```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z",
    "language": "en",
    "ui_theme": "light",
    "camera_mode": "standard"
  },
  {
    "id": 2,
    "email": "another@example.com",
    "full_name": "Another User",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z",
    "language": "en",
    "ui_theme": "light",
    "camera_mode": "standard"
  }
]
```

## Error Responses

### 401 Unauthorized

Returned when the request lacks valid authentication credentials.

```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden

Returned when the authenticated user doesn't have the required permissions.

```json
{
  "detail": "The user doesn't have enough privileges"
}
```

### 404 Not Found

Returned when the requested user doesn't exist.

```json
{
  "detail": "User not found"
}
```

## Implementation Details

The Users API is implemented in `app/api/endpoints/users.py`. It uses the following components:

- **Models**: `app/models/user.py` - SQLAlchemy model for user data
- **Schemas**: `app/schemas/user.py` - Pydantic schemas for request/response validation
- **Dependencies**: `app/api/deps.py` - Authentication and permission dependencies

## Example Usage

### Retrieving the Current User Profile

```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Updating the Current User Profile

```bash
curl -X PUT "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Updated Name",
    "ui_theme": "dark"
  }'
```

### Retrieving a Specific User (Superuser Only)

```bash
curl -X GET "http://localhost:8000/api/users/2" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Listing All Users (Superuser Only)

```bash
curl -X GET "http://localhost:8000/api/users/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```