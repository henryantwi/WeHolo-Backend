from typing import Any, Dict
import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, DBAPIError, DisconnectionError
from sqlalchemy import text

from app.api.deps import get_db
from app.db.session import engine

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
def health_check(db: Session = Depends(get_db)) -> Any:
    """
    Basic health check endpoint with database connection test.
    """
    db_status = "ok"
    db_message = "Connected to database"
    
    try:
        # Test database connection
        result = db.execute(text("SELECT 1")).scalar()
        if result != 1:
            db_status = "error"
            db_message = "Database connection test failed"
    except (OperationalError, DBAPIError, DisconnectionError) as e:
        db_status = "error"
        db_message = f"Database error: {str(e)}"
        
    return {
        "status": "ok",
        "message": "Service is running",
        "database": {
            "status": db_status,
            "message": db_message
        }
    }

@router.get("/db", response_model=Dict[str, Any])
def db_health_check(db: Session = Depends(get_db)) -> Any:
    """
    Database connection health check.
    """
    try:
        # Execute a simple query to check the database connection
        result = db.execute("SELECT 1").scalar()
        
        if result == 1:
            return {
                "status": "ok",
                "message": "Database connection successful",
                "timestamp": time.time()
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection check failed"
            )
    except (OperationalError, DBAPIError, DisconnectionError) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}"
        )

@router.get("/db/stats", response_model=Dict[str, Any])
def db_connection_stats() -> Any:
    """
    Get database connection pool statistics.
    """
    try:
        # Check if we're using SQLite
        is_sqlite = str(engine.url).startswith('sqlite')
        
        if is_sqlite:
            # SQLite doesn't have the same connection pool stats
            stats = {
                "engine_type": "SQLite",
                "connection_pool": "Not applicable for SQLite",
                "status": "ok",
            }
        else:
            # For PostgreSQL/MySQL
            stats = {
                "engine_type": str(engine.url).split('://')[0],
                "pool_size": engine.pool.size(),
                "checkedin": engine.pool.checkedin(),
                "checkedout": engine.pool.checkedout(),
                "overflow": engine.pool.overflow(),
                "status": "ok",
            }
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get connection stats: {str(e)}"
        )
