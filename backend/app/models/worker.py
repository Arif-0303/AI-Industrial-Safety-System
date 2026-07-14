from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    designation = Column(String)

    helmet = Column(Boolean, default=True)

    status = Column(String, default="Safe")

    sector_id = Column(Integer, ForeignKey("sectors.id"))

    sector = relationship("Sector", back_populates="workers")