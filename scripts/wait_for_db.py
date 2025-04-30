import time
import logging
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, DBAPIError

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_retries = 30
retry_interval = 2  # seconds
backoff_factor = 1.5  # Exponential backoff

def main():
    """Wait for the database to be ready."""
    logger.info("Waiting for database to be ready...")
    logger.info(f"Trying to connect to: {settings.DATABASE_URL}")
    
    current_interval = retry_interval
    
    for i in range(max_retries):
        try:
            # Determine if we're using PostgreSQL or SQLite
            is_postgres = settings.DATABASE_URL.startswith('postgresql')
            
            # Create the engine with appropriate parameters based on the database type
            if is_postgres:
                engine = create_engine(
                    settings.DATABASE_URL,
                    connect_args={"connect_timeout": 5}
                )
            else:
                engine = create_engine(settings.DATABASE_URL)
                
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database is ready!")
            return
        except (OperationalError, DBAPIError) as e:
            logger.info(f"Database not ready yet: {e}")
            logger.info(f"Retrying in {current_interval} seconds... ({i+1}/{max_retries})")
            time.sleep(current_interval)
            
            # Apply exponential backoff with a maximum of 10 seconds
            current_interval = min(current_interval * backoff_factor, 10)
    
    logger.error(f"Could not connect to database after {max_retries} retries")
    sys.exit(1)  # Exit with error code

if __name__ == "__main__":
    main()