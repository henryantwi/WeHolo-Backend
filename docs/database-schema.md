# WeHolo Database Schema

This document provides a detailed description of the WeHolo database schema, including tables, relationships, and field descriptions.

## Overview

WeHolo uses SQLAlchemy as an Object-Relational Mapping (ORM) tool to interact with the database. The database schema is defined through SQLAlchemy models and managed using Alembic migrations.

The application supports both PostgreSQL (recommended for production) and SQLite (for development).

## Entity Relationship Diagram

Below is a simplified entity relationship diagram showing the main tables and their relationships:

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    User     │       │   Avatar    │       │ Subscription│
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id          │       │ id          │       │ id          │
│ email       │       │ name        │       │ user_id     │──┐
│ hashed_pwd  │       │ user_id     │──┐    │ type        │  │
│ full_name   │       │ avatar_type │  │    │ start_date  │  │
│ is_active   │       │ settings    │  │    │ end_date    │  │
│ is_superuser│       │ created_at  │  │    │ is_active   │  │
│ created_at  │◀──────│ updated_at  │  │    │ created_at  │  │
│ updated_at  │       └─────────────┘  │    │ updated_at  │  │
│ language    │                        │    └─────────────┘  │
│ ui_theme    │                        │                     │
│ camera_mode │                        │                     │
└─────────────┘                        │                     │
       ▲                               │                     │
       │                               │                     │
       │       ┌─────────────┐         │                     │
       │       │ Conversation│         │                     │
       │       ├─────────────┤         │                     │
       └───────│ user_id     │         │                     │
               │ avatar_id   │◀────────┘                     │
               │ title       │                               │
               │ metadata    │                               │
               │ created_at  │                               │
               │ updated_at  │                               │
               └──────┬──────┘                               │
                      │                                      │
                      │                                      │
                      ▼                                      │
               ┌─────────────┐         ┌─────────────┐      │
               │   Message   │         │   Product   │      │
               ├─────────────┤         ├─────────────┤      │
               │ id          │         │ id          │      │
               │ content     │         │ name        │      │
               │ is_user     │         │ description │      │
               │ conversation_id       │ user_id     │◀─────┘
               │ created_at  │         │ image_url   │
               │ updated_at  │         │ created_at  │
               └─────────────┘         │ updated_at  │
                                       └─────────────┘
```

## Tables

### User

The User table stores information about registered users.

| Column          | Type      | Description                                   |
|-----------------|-----------|-----------------------------------------------|
| id              | Integer   | Primary key                                   |
| email           | String    | Unique email address (used for login)         |
| hashed_password | String    | Bcrypt-hashed password                        |
| full_name       | String    | User's full name                              |
| is_active       | Boolean   | Whether the user account is active            |
| is_superuser    | Boolean   | Whether the user has administrative privileges|
| created_at      | DateTime  | When the user account was created             |
| updated_at      | DateTime  | When the user account was last updated        |
| language        | String    | Preferred language (default: "en")            |
| ui_theme        | String    | UI theme preference (default: "light")        |
| camera_mode     | String    | Camera mode preference (default: "standard")  |

**Relationships:**
- One-to-many with Avatar
- One-to-many with Product
- One-to-many with Subscription
- One-to-many with Conversation

### Avatar

The Avatar table stores information about user avatars.

| Column          | Type      | Description                                   |
|-----------------|-----------|-----------------------------------------------|
| id              | Integer   | Primary key                                   |
| name            | String    | Avatar name                                   |
| user_id         | Integer   | Foreign key to User                           |
| avatar_type     | String    | Type of avatar (e.g., "akool", "soul_machines")|
| settings        | JSON      | Avatar configuration settings                 |
| created_at      | DateTime  | When the avatar was created                   |
| updated_at      | DateTime  | When the avatar was last updated              |

**Relationships:**
- Many-to-one with User
- One-to-many with Conversation

### Conversation

The Conversation table stores chat sessions between users and avatars.

| Column          | Type      | Description                                   |
|-----------------|-----------|-----------------------------------------------|
| id              | Integer   | Primary key                                   |
| title           | String    | Conversation title                            |
| user_id         | Integer   | Foreign key to User                           |
| avatar_id       | Integer   | Foreign key to Avatar                         |
| conversation_metadata | JSON | Additional metadata about the conversation   |
| created_at      | DateTime  | When the conversation was created             |
| updated_at      | DateTime  | When the conversation was last updated        |

**Relationships:**
- Many-to-one with User
- Many-to-one with Avatar
- One-to-many with Message

### Message

The Message table stores individual messages within conversations.

| Column          | Type      | Description                                   |
|-----------------|-----------|-----------------------------------------------|
| id              | Integer   | Primary key                                   |
| content         | Text      | Message content                               |
| is_user         | Boolean   | Whether the message is from the user (true) or avatar (false) |
| conversation_id | Integer   | Foreign key to Conversation                   |
| created_at      | DateTime  | When the message was created                  |
| updated_at      | DateTime  | When the message was last updated             |

**Relationships:**
- Many-to-one with Conversation

### Product

The Product table stores information about products that can be mentioned in conversations.

| Column          | Type      | Description                                   |
|-----------------|-----------|-----------------------------------------------|
| id              | Integer   | Primary key                                   |
| name            | String    | Product name                                  |
| description     | Text      | Product description                           |
| user_id         | Integer   | Foreign key to User                           |
| image_url       | String    | URL to product image                          |
| created_at      | DateTime  | When the product was created                  |
| updated_at      | DateTime  | When the product was last updated             |

**Relationships:**
- Many-to-one with User

### Subscription

The Subscription table stores information about user subscriptions.

| Column          | Type      | Description                                   |
|-----------------|-----------|-----------------------------------------------|
| id              | Integer   | Primary key                                   |
| user_id         | Integer   | Foreign key to User                           |
| type            | Enum      | Subscription type (basic, premium)            |
| start_date      | DateTime  | When the subscription started                 |
| end_date        | DateTime  | When the subscription ends                    |
| is_active       | Boolean   | Whether the subscription is active            |
| created_at      | DateTime  | When the subscription record was created      |
| updated_at      | DateTime  | When the subscription record was last updated |

**Relationships:**
- Many-to-one with User

## Indexes

The following indexes are defined to optimize query performance:

- User.email (unique)
- User.id
- Avatar.user_id
- Conversation.user_id
- Conversation.avatar_id
- Message.conversation_id
- Product.user_id
- Subscription.user_id

## Migrations

Database migrations are managed using Alembic. The migration files are stored in the `alembic/versions` directory.

To apply migrations:

```bash
alembic upgrade head
```

To create a new migration after modifying models:

```bash
alembic revision --autogenerate -m "Description of changes"
```

## Base Model

All models inherit from a common Base class that provides:

- Primary key (id)
- Common methods
- Relationship configurations

## SQLAlchemy Configuration

The SQLAlchemy engine is configured in `app/db/session.py` with the following features:

- Connection pooling
- Connection retry logic
- Health checks (pool_pre_ping)
- Support for both SQLite and PostgreSQL