from datetime import datetime

from fastapi import APIRouter
from sqlalchemy import text

from app.database.session import SessionLocal

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
def health_check():
    db_status = "Disconnected"

    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db_status = "Connected"
        db.close()

    except Exception:
        db_status = "Disconnected"

    return {
        "status": "Healthy",
        "database": db_status,
        "server_time": datetime.utcnow().isoformat(),
        "service": "AI Industrial Safety Monitoring System",
        "version": "1.0.0",
    }