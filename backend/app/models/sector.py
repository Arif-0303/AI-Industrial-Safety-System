from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.database.base import Base


class Sector(Base):
    __tablename__ = "sectors"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    temperature = Column(Float)

    gas = Column(Float)

    pressure = Column(Float)

    workers_present = Column(Integer)

    maintenance = Column(String)

    risk = Column(String)

    workers = relationship(
        "Worker",
        back_populates="sector",
        cascade="all, delete"
    )

    sensor_data = relationship(
        "SensorData",
        back_populates="sector",
        cascade="all, delete"
    )
    maintenance_records = relationship(
    "Maintenance",
    back_populates="sector",
    cascade="all, delete"
    )
    incidents = relationship(
    "Incident",
    back_populates="sector",
    cascade="all, delete"
    )
    permits = relationship(
    "Permit",
    back_populates="sector",
    cascade="all, delete"
    )