from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from random import uniform
from datetime import datetime
from ml.predict import predict_failure
from app.database.session import get_db

from app.models.sector import Sector
from app.models.sensor_data import SensorData

from app.ai.risk_engine import calculate_risk_score
from app.ai.recommendation_engine import recommendation
from app.ai.alert_engine import generate_alerts
from app.ai.predictive_maintenance import predictive_maintenance
from app.ai.incident_prediction import predict_incident

from app.websocket.connection_manager import manager

# NEW
from app.services.notification_service import (
    upsert_notification,
    delete_sector_notification,
)

router = APIRouter(
    prefix="/sensors",
    tags=["Live Sensors"],
)


# ==========================================================
# Simulate Live Sensor Values
# ==========================================================

from random import uniform, randint, choice

def simulate_sensor_values(sector: Sector):

    # ===============================
    # Blast Furnace (WARNING)
    # ===============================
    if sector.name == "Blast Furnace":

        sector.temperature = round(uniform(900, 1100), 1)
        sector.gas = round(uniform(18, 28), 1)
        sector.pressure = round(uniform(4.0, 5.5), 1)
        sector.workers_present = randint(10, 16)
        sector.maintenance = choice(["Good", "Average"])

    # ===============================
    # Coke Oven Battery (WARNING)
    # ===============================
    elif sector.name == "Coke Oven Battery":

        sector.temperature = round(uniform(700, 850), 1)
        sector.gas = round(uniform(10, 18), 1)
        sector.pressure = round(uniform(2.5, 4.5), 1)
        sector.workers_present = randint(10, 18)
        sector.maintenance = choice(["Good", "Average"])

    # ===============================
    # Power Plant (SAFE)
    # ===============================
    elif sector.name == "Power Plant":

        sector.temperature = round(uniform(60, 90), 1)
        sector.gas = round(uniform(2, 6), 1)
        sector.pressure = round(uniform(2, 4), 1)
        sector.workers_present = randint(8, 12)
        sector.maintenance = "Good"

    # ===============================
    # Basic Oxygen Furnace (WARNING)
    # ===============================
    elif sector.name == "Basic Oxygen Furnace":

        sector.temperature = round(uniform(1000, 1200), 1)
        sector.gas = round(uniform(8, 15), 1)
        sector.pressure = round(uniform(3, 5), 1)
        sector.workers_present = randint(10, 16)
        sector.maintenance = "Good"

    # ===============================
    # Rolling Mill (SAFE)
    # ===============================
    elif sector.name == "Rolling Mill":

        sector.temperature = round(uniform(300, 450), 1)
        sector.gas = round(uniform(1, 3), 1)
        sector.pressure = round(uniform(1, 3), 1)
        sector.workers_present = randint(12, 20)
        sector.maintenance = "Excellent"

    # ===============================
    # Remaining Plants (SAFE)
    # ===============================
    else:

        sector.temperature = round(uniform(25, 45), 1)
        sector.gas = round(uniform(0.2, 3), 1)
        sector.pressure = round(uniform(1, 3), 1)
        sector.workers_present = randint(5, 10)
        sector.maintenance = "Excellent"
# ==========================================================
# Build AI Response
# ==========================================================

def build_ai_response(sector):

    # Generate unified AI + CCTV analysis
    alerts = generate_alerts(sector)

    risk_score = alerts["risk_score"]

    # ==========================================
    # Machine Learning Prediction
    # ==========================================

    try:

        ml_prediction = predict_failure(
            sector=sector.name,
            machine="Conveyor Motor",
            shift="Morning",
            temperature=sector.temperature,
            pressure=sector.pressure,
            gas_co=sector.gas,
            gas_co2=6.5,
            oxygen=20.5,
            vibration=2.3,
            humidity=55,
            smoke_level=12,
            noise_level=78,
            motor_rpm=1450,
            bearing_temperature=58,
            power_consumption=120,
            oil_level=72,
            workers_present=sector.workers_present,
            maintenance_status=sector.maintenance,
            risk_score=risk_score,
            failure_probability=0.5,
            maintenance_due_days=12,
        )

    except Exception as e:

        print("ML Prediction Error:", e)

        ml_prediction = {
            "prediction": 0,
            "probability": 0.0,
            "status": "ML model skipped",
        }

    maintenance = predictive_maintenance(sector)

    incident = predict_incident(sector)

    return {

        "sector_id": sector.id,

        "sector_name": sector.name,

        "temperature": sector.temperature,

        "gas": sector.gas,

        "pressure": sector.pressure,

        "workers_present": sector.workers_present,

        "maintenance": sector.maintenance,

        "risk_score": risk_score,

        "ml_prediction": ml_prediction,

        "predictive_maintenance": maintenance,

        "incident_prediction": incident,

        # Entire alert object
        "alerts": alerts,

        "timestamp": datetime.utcnow().isoformat(),
    }

# ==========================================================
# Save Reading
# ==========================================================

def save_sensor_history(
    db: Session,
    sector: Sector,
):

    history = SensorData(
        sector_id=sector.id,
        temperature=sector.temperature,
        gas=sector.gas,
        pressure=sector.pressure,
        vibration=round(uniform(0.5, 5.0), 2),
    )

    db.add(history)
    db.commit()
    db.refresh(history)

# ==========================================================
# Store Notifications
# ==========================================================

async def store_notifications(
    db: Session,
    sector: Sector,
    ai_data,
):
    ai = ai_data["alerts"]["ai_alert"]
    cctv = ai_data["alerts"]["cctv"]

    # Trigger notification based on risk score
    if ai_data["risk_score"] >= 80:

        upsert_notification(
            db=db,
            title="🤖 AI SAFETY ALERT",
            message=(
                f"Sector: {sector.name}\n\n"
                f"Risk Score: {ai_data['risk_score']}\n\n"
                f"Cause:\n{ai['cause']}\n\n"
                f"Action:\n{ai['action']}"
            ),
            severity="Critical",
            sector=sector.name,
        )

        await manager.send_notification(
            title="🤖 AI SAFETY ALERT",
            message=f"{sector.name} is in CRITICAL condition.",
        )

    else:

        delete_sector_notification(
            db,
            "🤖 AI SAFETY ALERT",
            sector.name,
        )

    # CCTV Notification
    if cctv["status"] == "CRITICAL":

        upsert_notification(
            db=db,
            title="🎥 CCTV INSIGHT",
            message=f"{sector.name}\n\n{cctv['message']}",
            severity="Critical",
            sector=sector.name,
        )

        await manager.send_notification(
            title="🎥 CCTV INSIGHT",
            message=f"{sector.name}: {cctv['message']}",
        )

    else:

        delete_sector_notification(
            db,
            "🎥 CCTV INSIGHT",
            sector.name,
        )

# ==========================================================
# Live Sensor Data
# ==========================================================
@router.get("/live")
async def get_live_sensor_data(
    db: Session = Depends(get_db),
):

    sectors = db.query(Sector).all()

    response = []

    for sector in sectors:

        simulate_sensor_values(sector)

        db.commit()
        db.refresh(sector)

        save_sensor_history(
            db,
            sector,
        )

        ai_data = build_ai_response(
            sector,
        )

        await store_notifications(
            db,
            sector,
            ai_data,
        )

        response.append(ai_data)

    await manager.broadcast(
        {
            "type": "sensor_update",
            "data": response,
        }
    )

    return {
        "success": True,
        "count": len(response),
        "data": response,
    }


# ==========================================================
# Sector Live Data
# ==========================================================

@router.get("/live/{sector_id}")
async def get_sector_live_data(
    sector_id: int,
    db: Session = Depends(get_db),
):

    sector = (
        db.query(Sector)
        .filter(Sector.id == sector_id)
        .first()
    )

    if sector is None:
        return {
            "success": False,
            "message": "Sector not found",
        }

    simulate_sensor_values(sector)

    db.commit()
    db.refresh(sector)

    save_sensor_history(
        db,
        sector,
    )

    ai_data = build_ai_response(
        sector,
    )

    await store_notifications(
        db,
        sector,
        ai_data,
    )

    await manager.broadcast(
        {
            "type": "sector_update",
            "data": ai_data,
        }
    )

    return {
        "success": True,
        "data": ai_data,
    }


# ==========================================================
# Broadcast Trigger
# ==========================================================

@router.post("/broadcast")
async def broadcast_all(
    db: Session = Depends(get_db),
):

    sectors = db.query(Sector).all()

    payload = []

    for sector in sectors:

        simulate_sensor_values(sector)

        db.commit()
        db.refresh(sector)

        save_sensor_history(
            db,
            sector,
        )

        ai_data = build_ai_response(
            sector,
        )

        await store_notifications(
            db,
            sector,
            ai_data,
        )

        payload.append(ai_data)

    await manager.broadcast(
        {
            "type": "sensor_update",
            "data": payload,
        }
    )

    return {
        "success": True,
        "message": "Live data broadcasted successfully.",
        "connected_clients": manager.total_connections(),
    }