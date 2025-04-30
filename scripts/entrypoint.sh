#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status

# Wait for the database to be ready
echo "Waiting for database to be ready..."
python -m scripts.wait_for_db

# Apply database migrations
echo "Applying database migrations..."
alembic upgrade head || {
    echo "Database migration failed. Retrying in 5 seconds..."
    sleep 5
    alembic upgrade head
}

# Start the application with improved settings
echo "Starting the application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info