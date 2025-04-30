# Getting Started with WeHolo

This guide will help you set up the WeHolo project for local development or production deployment.

## Prerequisites

### For Local Development

- **Python 3.8+**: The project is built with Python 3.8 or higher.
- **pip**: Python package manager for installing dependencies.
- **Virtual environment**: Recommended for isolating project dependencies.
- **PostgreSQL** (optional): For production-like development. SQLite can be used for simpler setups.

### For Docker Deployment

- **Docker**: Container platform for running the application.
- **Docker Compose**: Tool for defining and running multi-container Docker applications.

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/henryantwi/weholo-project.git
cd weholo-project
```

### 2. Create and Activate a Virtual Environment

#### On Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### On macOS/Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root with the following variables:

```
# API configuration
API_V1_STR=/api
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=11520  # 8 days

# Database
# For SQLite (development)
DATABASE_URL=sqlite:///./weholo.db
# For PostgreSQL (more production-like)
# DATABASE_URL=postgresql://username:password@localhost:5432/weholo

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# API Keys (if available)
AKOOL_API_KEY=your-akool-api-key
SOUL_MACHINES_API_KEY=your-soul-machines-api-key

# Debug mode
DEBUG=True
ENVIRONMENT=development
```

Replace the placeholder values with your actual configuration.

### 5. Initialize the Database

Run Alembic migrations to set up the database schema:

```bash
alembic upgrade head
```

### 6. Run the Development Server

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000. You can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Deployment

### 1. Set Up Environment Files

Create `.env.web` for the web service:

```
# API configuration
API_V1_STR=/api
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=11520

# Database
DATABASE_URL=postgresql://weholo:weholo@db:5432/weholo

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# API Keys
AKOOL_API_KEY=your-akool-api-key
SOUL_MACHINES_API_KEY=your-soul-machines-api-key

# Debug mode
DEBUG=False
ENVIRONMENT=production
```

Create `.env.db` for the database service:

```
POSTGRES_USER=weholo
POSTGRES_PASSWORD=weholo
POSTGRES_DB=weholo
```

### 2. Build and Start the Containers

```bash
docker-compose up -d
```

The API will be available at http://localhost:8000.

### 3. Apply Database Migrations

```bash
docker-compose exec web alembic upgrade head
```

### 4. View Logs

```bash
docker-compose logs -f
```

### 5. Stop the Containers

```bash
docker-compose down
```

## Development Workflow

1. Make changes to the code
2. Run tests to ensure your changes don't break existing functionality
3. Start the development server to test your changes manually
4. Commit your changes with a descriptive message

## Troubleshooting

### Database Connection Issues

If you encounter database connection issues:

1. Check that your database server is running
2. Verify that the DATABASE_URL in your .env file is correct
3. For PostgreSQL, ensure the database and user exist with the correct permissions

### Dependency Issues

If you encounter issues with dependencies:

1. Make sure your virtual environment is activated
2. Update your dependencies: `pip install -r requirements.txt --upgrade`
3. If a specific package is causing issues, try installing it separately

### Docker Issues

If you encounter issues with Docker:

1. Check that Docker and Docker Compose are installed and running
2. Verify that the ports specified in docker-compose.yml are not already in use
3. Check the logs for specific error messages: `docker-compose logs`