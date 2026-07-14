from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    message = Column(String, nullable=False)

    severity = Column(String, default="Info")

    sector = Column(String, default="General")

    is_read = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)