from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DBAPIError, OperationalError, DisconnectionError
from sqlalchemy.pool import QueuePool
from icecream import ic
import time
import logging
import re

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine if we're using SQLite
is_sqlite = settings.DATABASE_URL.startswith('sqlite')

# Adjust connection pool configuration based on database type
if is_sqlite:
    # SQLite-specific settings
    connect_args = {"check_same_thread": False}
    pool_size = None  # Not used for SQLite
    max_overflow = None  # Not used for SQLite
    pool_recycle = None  # Not used for SQLite
else:
    # PostgreSQL/MySQL settings
    connect_args = {}
    pool_size = 5
    max_overflow = 10
    pool_recycle = 1800  # Recycle connections after 30 minutes

# Common settings
pool_timeout = 30
pool_pre_ping = True  # Enable connection health checks

# Create SQLAlchemy engine with appropriate configuration
if is_sqlite:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        pool_pre_ping=pool_pre_ping,
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
        pool_recycle=pool_recycle,
        pool_pre_ping=pool_pre_ping,
    )
ic(settings.DATABASE_URL)

# Handle connection events (only for non-SQLite databases)
if not is_sqlite:
    @event.listens_for(engine, "connect")
    def connect(dbapi_connection, connection_record):
        logger.info("Connection established")
        connection_record.info['pid'] = id(dbapi_connection)

    @event.listens_for(engine, "checkout")
    def checkout(dbapi_connection, connection_record, connection_proxy):
        pid = connection_record.info.get('pid')
        if pid != id(dbapi_connection):
            logger.info("Connection was invalidated - creating a new one")
            connection_record.info['pid'] = id(dbapi_connection)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session with reconnection logic
def get_db():
    db = SessionLocal()
    max_retries = 3
    retry_delay = 1  # seconds
    
    try:
        # Test connection with a simple query
        db.execute(text("SELECT 1"))
        yield db
    except (OperationalError, DBAPIError, DisconnectionError) as e:
        logger.error(f"Database connection error: {str(e)}")
        
        # Attempt to reconnect
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempting to reconnect (attempt {attempt + 1}/{max_retries})")
                db.close()
                time.sleep(retry_delay)
                db = SessionLocal()
                db.execute(text("SELECT 1"))
                logger.info("Successfully reconnected to database")
                yield db
                break
            except Exception as retry_error:
                logger.error(f"Reconnection attempt {attempt + 1} failed: {str(retry_error)}")
                if attempt == max_retries - 1:
                    raise  # Re-raise the exception if all retries fail
    finally:
        db.close()
