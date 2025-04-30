#!/bin/sh

# Wait for the database to be ready
echo "Waiting for database to be ready..."
python -m scripts.wait_for_db

# Apply database migrations
echo "Applying database migrations..."
alembic upgrade head

# Start the application
echo "Starting the application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000