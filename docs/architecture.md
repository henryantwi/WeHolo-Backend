# WeHolo Architecture

This document provides an overview of the WeHolo platform's architecture, design patterns, and component interactions.

## System Architecture

WeHolo follows a modern, layered architecture pattern that separates concerns and promotes maintainability and scalability.

### High-Level Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Client         │────▶│  WeHolo API     │────▶│  Database       │
│  Applications   │     │  (FastAPI)      │     │  (PostgreSQL)   │
│                 │◀────│                 │◀────│                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  External APIs  │
                        │  - AKOOL        │
                        │  - Soul Machines│
                        └─────────────────┘
```

### Layered Architecture

The backend application follows a layered architecture pattern:

1. **API Layer**: Handles HTTP requests and responses, input validation, and routing
2. **Service Layer**: Contains business logic and orchestrates operations
3. **Data Access Layer**: Manages database interactions using SQLAlchemy ORM
4. **Domain Layer**: Defines the core domain models and business rules

## Component Overview

### API Layer

The API layer is built with FastAPI and is organized into modules by feature:

- **Endpoints**: API route handlers organized by domain (users, avatars, chat, etc.)
- **Dependencies**: Reusable components for authentication, database access, etc.
- **Schemas**: Pydantic models for request/response validation and serialization

### Core Components

- **Configuration**: Application settings and environment variables
- **Security**: Authentication and authorization mechanisms
- **Database**: Connection management and session handling

### Data Models

The data models represent the domain entities and their relationships:

- **User**: User accounts and preferences
- **Avatar**: 3D characters that users can interact with
- **Conversation**: Chat sessions between users and avatars
- **Message**: Individual messages within conversations
- **Product**: Products that can be mentioned and displayed during conversations
- **Subscription**: User subscription information

## Design Patterns

WeHolo implements several design patterns to promote code quality and maintainability:

### Dependency Injection

FastAPI's dependency injection system is used extensively to:
- Provide database sessions
- Handle authentication and authorization
- Implement request validation

Example:
```python
@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    return current_user
```

### Repository Pattern

Database access is abstracted through SQLAlchemy models and queries, providing a clean separation between business logic and data access.

### Schema-Based Validation

Pydantic models are used to validate incoming requests and format outgoing responses, ensuring type safety and data integrity.

### JWT Authentication

JSON Web Tokens (JWT) are used for stateless authentication, allowing the API to scale horizontally without shared session storage.

## Data Flow

### Request Handling Flow

1. Client sends a request to an API endpoint
2. FastAPI routes the request to the appropriate handler
3. Dependencies are resolved (authentication, database session, etc.)
4. Input data is validated using Pydantic schemas
5. Business logic is executed
6. Response is formatted and returned to the client

### Authentication Flow

1. User submits credentials to the `/auth/login` endpoint
2. Credentials are validated against the database
3. If valid, a JWT token is generated and returned
4. For subsequent requests, the client includes the token in the Authorization header
5. The `get_current_user` dependency validates the token and retrieves the user

## External Integrations

WeHolo integrates with external services to provide avatar functionality:

### AKOOL API

- Used for basic avatar creation and customization
- Provides pre-designed avatars in the gallery
- Handles video generation for avatar responses

### Soul Machines API

- Used for premium avatar experiences
- Provides more advanced interaction capabilities
- Supports real-time avatar responses with enhanced animations

## Scalability Considerations

The architecture is designed with scalability in mind:

- **Stateless API**: The API is stateless, allowing for horizontal scaling
- **Database Connection Pooling**: Efficient management of database connections
- **Caching**: Conversations can be cached locally to reduce API calls
- **Docker Containerization**: Facilitates deployment and scaling in cloud environments

## Security Considerations

Security is a priority in the WeHolo architecture:

- **Password Hashing**: User passwords are hashed using bcrypt
- **JWT Authentication**: Secure, stateless authentication
- **Role-Based Access Control**: Different permission levels for users and administrators
- **Input Validation**: All input is validated using Pydantic schemas
- **Database Query Safety**: SQLAlchemy ORM prevents SQL injection
- **Error Handling**: Proper error handling to prevent information leakage