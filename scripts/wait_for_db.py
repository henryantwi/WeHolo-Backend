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
    
    current_interval = retry_interval
    
    for i in range(max_retries):
        try:
            # Try to connect to the database with timeout
            engine = create_engine(
                settings.DATABASE_URL,
                connect_args={"connect_timeout": 5}
            )
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