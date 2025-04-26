import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_retries = 30
retry_interval = 2  # seconds

def main():
    """Wait for the database to be ready."""
    logger.info("Waiting for database to be ready...")
    
    for i in range(max_retries):
        try:
            # Try to connect to the database
            engine = create_engine(settings.DATABASE_URL)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database is ready!")
            return
        except OperationalError as e:
            logger.info(f"Database not ready yet: {e}")
            logger.info(f"Retrying in {retry_interval} seconds... ({i+1}/{max_retries})")
            time.sleep(retry_interval)
    
    logger.error(f"Could not connect to database after {max_retries} retries")
    raise Exception("Database connection failed")

if __name__ == "__main__":
    main()