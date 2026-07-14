from sqlalchemy.orm import Session

from app.database.database import SessionLocal, engine
from app.database.base import Base

# Import ALL models
from app.models.user import User
from app.models.sector import Sector
from app.models.sensor_data import SensorData
from app.models.notification import Notification
from app.models.incident import Incident

Base.metadata.create_all(bind=engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()