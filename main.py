from sqlalchemy import text
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api.endpoints import (
    auth,
    users,
    dashboard,
    gallery,
    studio,
    demo,
    chat,
    subscription,
    products,
    bot
)
from app.core.config import settings
from app.db.session import get_db, engine
from app.models.base import Base

# Note: Tables are managed by Alembic migrations
# Run 'alembic upgrade head' to apply migrations

app = FastAPI(
    title="WeHolo API",
    description="API for WeHolo platform",
    version="0.1.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["dashboard"])
app.include_router(gallery.router, prefix=f"{settings.API_V1_STR}/gallery", tags=["gallery"])
app.include_router(studio.router, prefix=f"{settings.API_V1_STR}/studio", tags=["studio"])
app.include_router(demo.router, prefix=f"{settings.API_V1_STR}/demo", tags=["demo"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(subscription.router, prefix=f"{settings.API_V1_STR}/subscription", tags=["subscription"])
app.include_router(products.router, prefix=f"{settings.API_V1_STR}/products", tags=["products"])
app.include_router(bot.router, prefix=f"{settings.API_V1_STR}/bot", tags=["bot"])


@app.get("/")
def read_root():
    return {"message": "Welcome to WeHolo API"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Execute a simple query to verify database connection
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="debug"
    )
