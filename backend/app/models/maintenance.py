from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True, index=True)

    sector_id = Column(Integer, ForeignKey("sectors.id"))

    engineer = Column(String, nullable=False)

    activity = Column(String)

    status = Column(String)

    scheduled_date = Column(Date)

    sector = relationship("Sector", back_populates="maintenance_records")