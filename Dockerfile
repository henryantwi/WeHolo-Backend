FROM python:3.12.10-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make the entrypoint script executable
RUN chmod +x /app/scripts/entrypoint.sh

# Create a directory for SQLite database
RUN mkdir -p /app/data

# Expose the application port
EXPOSE 8000

# Set environment variable to use PostgreSQL by default
ENV DATABASE_URL="postgresql://weholo:weholo@db:5432/weholo"

# Use the entrypoint script
CMD ["/app/scripts/entrypoint.sh"]
