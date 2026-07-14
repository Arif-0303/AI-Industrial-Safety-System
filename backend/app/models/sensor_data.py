from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.base import Base


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)

    sector_id = Column(Integer, ForeignKey("sectors.id"))

    temperature = Column(Float)

    gas = Column(Float)

    pressure = Column(Float)

    vibration = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)

    sector = relationship("Sector", back_populates="sensor_data")