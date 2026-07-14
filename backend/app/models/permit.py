from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Permit(Base):
    __tablename__ = "permits"

    id = Column(Integer, primary_key=True, index=True)

    sector_id = Column(Integer, ForeignKey("sectors.id"))

    permit_type = Column(String)

    issued_to = Column(String)

    expiry_date = Column(Date)

    status = Column(String)

    sector = relationship("Sector", back_populates="permits")