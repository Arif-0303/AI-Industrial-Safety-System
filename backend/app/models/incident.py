from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.base import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    sector_id = Column(Integer, ForeignKey("sectors.id"))

    severity = Column(String)

    cause = Column(String)

    action = Column(String)

    status = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    sector = relationship("Sector", back_populates="incidents")