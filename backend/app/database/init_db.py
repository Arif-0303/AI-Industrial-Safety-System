from app.database.database import engine, SessionLocal
from app.database.base import Base

from app.models.user import User
from app.models.sector import Sector
from app.models.sensor_data import SensorData
from app.models.notification import Notification
from app.models.incident import Incident

# Create all tables
Base.metadata.create_all(bind=engine)


def seed_database():
    db = SessionLocal()

    # Don't insert again if sectors already exist
    if db.query(Sector).count() == 0:

        sectors = [

    Sector(
        name="Raw Material Handling Plant",
        temperature=34.5,
        gas=1.5,
        pressure=1.1,
        workers_present=18,
        maintenance="Good",
        risk="Safe"
    ),

    Sector(
        name="Coal Handling Plant",
        temperature=39.2,
        gas=5.3,
        pressure=1.4,
        workers_present=15,
        maintenance="Good",
        risk="Safe"
    ),

    Sector(
        name="Coke Oven Battery",
        temperature=845,
        gas=26.8,
        pressure=3.4,
        workers_present=22,
        maintenance="Average",
        risk="Warning"
    ),

    Sector(
        name="By Product Plant",
        temperature=68,
        gas=18,
        pressure=2.3,
        workers_present=12,
        maintenance="Average",
        risk="Warning"
    ),

    Sector(
        name="Sinter Plant",
        temperature=420,
        gas=11,
        pressure=2.7,
        workers_present=20,
        maintenance="Good",
        risk="Safe"
    ),

    Sector(
        name="Blast Furnace",
        temperature=1225,
        gas=34,
        pressure=6.8,
        workers_present=14,
        maintenance="Average",
        risk="Danger"
    ),

    Sector(
        name="Basic Oxygen Furnace",
        temperature=1630,
        gas=19,
        pressure=5.1,
        workers_present=16,
        maintenance="Average",
        risk="Danger"
    ),

    Sector(
        name="Continuous Casting",
        temperature=730,
        gas=4,
        pressure=2.1,
        workers_present=13,
        maintenance="Good",
        risk="Safe"
    ),

    Sector(
        name="Rolling Mill",
        temperature=515,
        gas=3,
        pressure=1.8,
        workers_present=24,
        maintenance="Good",
        risk="Safe"
    ),

    Sector(
        name="Oxygen Plant",
        temperature=27,
        gas=0.5,
        pressure=8.6,
        workers_present=8,
        maintenance="Excellent",
        risk="Safe"
    ),

    Sector(
        name="Power Plant",
        temperature=98,
        gas=7.4,
        pressure=4.3,
        workers_present=10,
        maintenance="Good",
        risk="Warning"
    ),

    Sector(
        name="Water Treatment Plant",
        temperature=31,
        gas=0.4,
        pressure=2.0,
        workers_present=9,
        maintenance="Excellent",
        risk="Safe"
    ),

]

        db.add_all(sectors)
        db.commit()

    db.close()


seed_database()