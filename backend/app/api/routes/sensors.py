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

def simulate_sensor_values(sector: Sector):

    # ===============================
    # Blast Furnace -> CRITICAL
    # ===============================
    if sector.name == "Blast Furnace":
        sector.temperature = 1250
        sector.gas = 38
        sector.pressure = 7.8
        sector.workers_present = 14
        sector.maintenance = "Average"

    # ===============================
    # Coke Oven -> WARNING
    # ===============================
    elif sector.name == "Coke Oven Battery":
        sector.temperature = 860
        sector.gas = 18
        sector.pressure = 3.5
        sector.workers_present = 18
        sector.maintenance = "Average"

    # ===============================
    # Power Plant -> WARNING
    # ===============================
    elif sector.name == "Power Plant":
        sector.temperature = 95
        sector.gas = 8
        sector.pressure = 4.2
        sector.workers_present = 10
        sector.maintenance = "Good"

    # ===============================
    # Everything Else -> SAFE
    # ===============================
    else:
        sector.temperature = 35
        sector.gas = 2
        sector.pressure = 2
        sector.workers_present = 8
        sector.maintenance = "Good"

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

    # ==========================================
    # AI ALERT
    # ==========================================

    ai = ai_data["alerts"]["ai_alert"]

    if ai["status"] == "CRITICAL":

        upsert_notification(
            db=db,
            title="🤖 AI SAFETY ALERT",
            message=(
                f"Sector: {sector.name}\n\n"
                f"{ai['message']}\n\n"
                f"Recommendation:\n"
                f"{ai['recommendation']}"
            ),
            severity="Critical",
            sector=sector.name,
        )

    else:

        delete_sector_notification(
            db,
            "🤖 AI SAFETY ALERT",
            sector.name,
        )

    # ==========================================
    # CCTV INSIGHT
    # ==========================================

    cctv = ai_data["alerts"]["cctv"]

    if cctv["status"] == "CRITICAL":

        upsert_notification(
            db=db,
            title="🎥 CCTV INSIGHT",
            message=(
                f"Sector: {sector.name}\n\n"
                f"{cctv['message']}"
            ),
            severity="Critical",
            sector=sector.name,
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