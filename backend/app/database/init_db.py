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
                temperature=35,
                gas=1.2,
                pressure=1.2,
                workers_present=18,
                maintenance="Good",
                risk="Safe"
            ),

            Sector(
                name="Coal Handling Plant",
                temperature=42,
                gas=5.5,
                pressure=1.8,
                workers_present=15,
                maintenance="Good",
                risk="Safe"
            ),

            Sector(
                name="Coke Oven Battery",
                temperature=780,
                gas=18,
                pressure=2.8,
                workers_present=22,
                maintenance="Good",
                risk="Warning"
            ),

            Sector(
                name="By Product Plant",
                temperature=62,
                gas=10,
                pressure=2.1,
                workers_present=12,
                maintenance="Good",
                risk="Safe"
            ),

            Sector(
                name="Sinter Plant",
                temperature=390,
                gas=9,
                pressure=2.5,
                workers_present=20,
                maintenance="Good",
                risk="Safe"
            ),

            # ONLY CRITICAL PLANT
            Sector(
                name="Blast Furnace",
                temperature=1480,
                gas=38,
                pressure=8.4,
                workers_present=14,
                maintenance="Poor",
                risk="Danger"
            ),

            Sector(
                name="Basic Oxygen Furnace",
                temperature=1560,
                gas=12,
                pressure=4.5,
                workers_present=16,
                maintenance="Good",
                risk="Warning"
            ),

            Sector(
                name="Continuous Casting",
                temperature=690,
                gas=3,
                pressure=2.0,
                workers_present=13,
                maintenance="Excellent",
                risk="Safe"
            ),

            Sector(
                name="Rolling Mill",
                temperature=470,
                gas=2,
                pressure=1.7,
                workers_present=24,
                maintenance="Excellent",
                risk="Safe"
            ),

            Sector(
                name="Oxygen Plant",
                temperature=28,
                gas=0.4,
                pressure=8.4,
                workers_present=8,
                maintenance="Excellent",
                risk="Safe"
            ),

            Sector(
                name="Power Plant",
                temperature=88,
                gas=6,
                pressure=3.8,
                workers_present=10,
                maintenance="Good",
                risk="Warning"
            ),

            Sector(
                name="Water Treatment Plant",
                temperature=30,
                gas=0.3,
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