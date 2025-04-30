# WeHolo API Reference

This section provides detailed documentation for the WeHolo API endpoints.

## API Base URL

All API endpoints are prefixed with `/api` by default. This can be configured using the `API_V1_STR` environment variable.

## Authentication

Most endpoints require authentication using JWT (JSON Web Tokens). To authenticate:

1. Obtain a token by sending a POST request to `/api/auth/login` with your credentials
2. Include the token in the `Authorization` header of subsequent requests:
   ```
   Authorization: Bearer <your_token>
   ```

See the [Authentication](../authentication.md) documentation for more details.

## API Endpoints

### Authentication

- [Authentication](./authentication.md) - Endpoints for user authentication and token management

### Users

- [Users](./users.md) - Endpoints for user management and profile operations

### Dashboard

- [Dashboard](./dashboard.md) - Endpoints for user dashboard customization

### Avatars

- [Gallery](./gallery.md) - Endpoints for browsing and selecting pre-designed avatars
- [Studio](./studio.md) - Endpoints for creating and customizing avatars

### Interactions

- [Chat](./chat.md) - Endpoints for conversations with avatars
- [Demo](./demo.md) - Endpoints for viewing pre-recorded avatar demonstrations

### Business Features

- [Subscription](./subscription.md) - Endpoints for managing user subscriptions
- [Products](./products.md) - Endpoints for managing products that can be mentioned in conversations
- [Bot](./bot.md) - Endpoints for the recommendation bot

### System

- [Health](./health.md) - Endpoints for system health monitoring

## Response Format

All API responses follow a consistent JSON format:

### Success Response

```json
{
  "data": {
    // Response data here
  }
}
```

### Error Response

```json
{
  "detail": "Error message"
}
```

For validation errors, the response includes more detailed information:

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Pagination

Endpoints that return lists of items support pagination using the following query parameters:

- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum number of items to return (default: 100)

Example:
```
GET /api/users?skip=10&limit=20
```

## Filtering and Sorting

Some endpoints support filtering and sorting using query parameters. The specific parameters are documented in the individual endpoint documentation.

## Rate Limiting

The API implements rate limiting to prevent abuse. The current limits are:

- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

If you exceed these limits, you will receive a 429 Too Many Requests response.

## API Versioning

The current API version is v1. The version is included in the URL prefix (`/api`).

Future versions will be available at different URL prefixes (e.g., `/api/v2`).

## API Documentation

Interactive API documentation is available at:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

These interfaces provide a user-friendly way to explore the API and test endpoints directly from your browser.