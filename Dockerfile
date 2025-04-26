FROM python:3.13.3-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make the entrypoint script executable
RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 8000

# Use the entrypoint script
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
