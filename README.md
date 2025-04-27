# WeHolo

WeHolo is an online platform that provides users with a fun and interactive experience using 3D avatars powered by AI. Users can pick avatars, talk to them using text or voice, and see the avatars respond with animations like lip-syncing, gestures, and emotions.

## Features

- **User Accounts**: Sign up and log in to access personalized settings
- **Dashboard**: Customize avatars, adjust behavior, change camera modes, pick languages, and customize the UI
- **Gallery**: Choose from a variety of pre-designed avatars (via AKOOL API)
- **Studio**: Design and customize your own avatars
- **Demo Section**: View pre-recorded demonstrations of avatars in action
- **Interactive Chat**: Communicate with avatars via text or video
- **Subscription System**: Choose between basic (AKOOL) and premium (Soul Machines) features
- **Product Display**: Display products when avatars mention them
- **Beginner-Friendly Bot**: Get avatar recommendations based on your preferences
- **Cached Conversations**: Store conversations locally to reduce API calls

## Technology Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **APIs**: AKOOL API, Soul Machines API
- **Containerization**: Docker, Docker Compose

## Installation

### Prerequisites

#### For Local Development
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

#### For Docker Deployment
- Docker
- Docker Compose

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/henryantwi/weholo-project.git
   cd weholo-project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create environment files:
   ```bash
   # For local development
   cp .env.example .env
   # Edit .env with your configuration

   # For Docker deployment
   cp .env.web.example .env.web
   cp .env.db.example .env.db
   # Edit .env.web and .env.db with your configuration
   ```

5. Initialize the database:
   ```bash
   alembic upgrade head
   ```

## Running the Application

### Development

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker

The application can be run using Docker and Docker Compose:

1. Set up environment files:
   ```bash
   cp .env.web.example .env.web
   cp .env.db.example .env.db
   # Edit .env.web and .env.db with your configuration
   ```

2. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

3. The API will be available at http://localhost:8000

   > **Note:** Database migrations are automatically applied when the container starts. If you need to manually apply migrations, you can use:
   > ```bash
   > docker-compose exec web alembic upgrade head
   > ```

5. To stop the containers:
   ```bash
   docker-compose down
   ```

6. To view logs:
   ```bash
   docker-compose logs -f
   ```

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
weholo-project/
├── alembic/                  # Database migrations
├── app/
│   ├── api/                  # API endpoints
│   │   ├── endpoints/        # API route handlers
│   │   └── deps.py           # API dependencies
│   ├── core/                 # Core functionality
│   │   ├── config.py         # Application configuration
│   │   └── security.py       # Security utilities
│   ├── db/                   # Database
│   │   └── session.py        # Database session
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   └── services/             # Business logic
├── scripts/                  # Utility scripts
│   ├── entrypoint.sh         # Docker container entrypoint script
│   └── wait_for_db.py        # Script to wait for database to be ready
├── .dockerignore             # Files to exclude from Docker image
├── .env                      # Environment variables for local development
├── .env.example              # Example environment variables for local development
├── .env.web                  # Environment variables for web service in Docker
├── .env.web.example          # Example environment variables for web service
├── .env.db                   # Environment variables for database service in Docker
├── .env.db.example           # Example environment variables for database service
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker image definition
├── main.py                   # Application entry point
├── pyproject.toml            # Project metadata
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [AKOOL](https://akool.com/) for avatar creation and video generation
- [Soul Machines](https://www.soulmachines.com/) for interactive avatar experiences
