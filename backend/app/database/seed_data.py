import app.models
from app.database.database import SessionLocal
from app.models.sector import Sector

db = SessionLocal()

# Don't insert duplicate data
if db.query(Sector).count() == 0:

    sectors = [

        Sector(
            name="Blast Furnace",
            temperature=84,
            gas=18,
            pressure=4.2,
            workers_present=24,
            maintenance="Good",
            risk="Medium"
        ),

        Sector(
            name="Steel Melting Shop",
            temperature=96,
            gas=22,
            pressure=5.4,
            workers_present=20,
            maintenance="Due",
            risk="High"
        ),

        Sector(
            name="Rolling Mill",
            temperature=62,
            gas=9,
            pressure=3.5,
            workers_present=18,
            maintenance="Good",
            risk="Low"
        ),

        Sector(
            name="Coke Oven",
            temperature=110,
            gas=28,
            pressure=6.5,
            workers_present=15,
            maintenance="Critical",
            risk="Critical"
        ),

        Sector(
            name="Power Plant",
            temperature=58,
            gas=6,
            pressure=3.1,
            workers_present=12,
            maintenance="Good",
            risk="Low"
        ),

        Sector(
            name="Oxygen Plant",
            temperature=35,
            gas=2,
            pressure=2.8,
            workers_present=8,
            maintenance="Good",
            risk="Low"
        ),

        Sector(
            name="Raw Material Yard",
            temperature=40,
            gas=4,
            pressure=2.1,
            workers_present=16,
            maintenance="Good",
            risk="Low"
        ),

        Sector(
            name="Sinter Plant",
            temperature=73,
            gas=12,
            pressure=4.0,
            workers_present=17,
            maintenance="Due",
            risk="Medium"
        ),

        Sector(
            name="Water Treatment Plant",
            temperature=29,
            gas=1,
            pressure=2.0,
            workers_present=9,
            maintenance="Good",
            risk="Low"
        ),

        Sector(
            name="Finished Goods Warehouse",
            temperature=27,
            gas=0,
            pressure=1.8,
            workers_present=11,
            maintenance="Good",
            risk="Low"
        )

    ]

    db.add_all(sectors)
    db.commit()

    print("✅ Steel plant demo data inserted successfully!")

else:
    print("ℹ️ Sector data already exists.")

db.close()