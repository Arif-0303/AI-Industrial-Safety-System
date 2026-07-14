import random
import time

from app.database.database import SessionLocal
from app.models.sector import Sector


def simulate_sensor_data():
    while True:
        db = SessionLocal()

        sectors = db.query(Sector).all()

        for sector in sectors:

            sector.temperature = round(
                sector.temperature + random.uniform(-2, 2),
                1
            )

            sector.gas = round(
                sector.gas + random.uniform(-3, 3),
                1
            )

            sector.pressure = round(
                sector.pressure + random.uniform(-0.3, 0.3),
                2
            )

        db.commit()
        db.close()

        print("Sensor values updated...")

        time.sleep(5)