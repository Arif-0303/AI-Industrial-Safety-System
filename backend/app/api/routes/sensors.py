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
from app.services.notification_service import create_notification

router = APIRouter(
    prefix="/sensors",
    tags=["Live Sensors"],
)


# ==========================================================
# Simulate Live Sensor Values
# ==========================================================

def simulate_sensor_values(sector: Sector):

    sector.temperature = round(
        max(20, sector.temperature + uniform(-3, 3)),
        2,
    )

    sector.gas = round(
        max(0, sector.gas + uniform(-2, 2)),
        2,
    )

    sector.pressure = round(
        max(1, sector.pressure + uniform(-0.4, 0.4)),
        2,
    )


# ==========================================================
# Build AI Response
# ==========================================================

def build_ai_response(sector):

    risk_score = calculate_risk_score(sector)

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

    alerts = generate_alerts(sector)

    recommendation_text = recommendation(risk_score)

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
        "recommendation": recommendation_text,
        "alerts": alerts,
        "predictive_maintenance": maintenance,
        "incident_prediction": incident,
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
# ==========================================================
# Store Notifications
# Only popup Danger & Critical alerts
# ==========================================================
async def store_notifications(
    db: Session,
    sector: Sector,
    ai_data,
):
    """
    Store ONLY high-priority notifications.

    Types:
    1. CCTV Insight
    2. AI Safety Alert
    """

    risk_score = ai_data["risk_score"]

    # ======================================================
    # AI SAFETY ALERT
    # ======================================================

    if risk_score >= 75:
#this is the end
        title = "🤖 AI SAFETY ALERT"

        message = (
            f"Sector: {sector.name}\n"
            f"Risk Score: {risk_score:.1f}\n\n"
            f"{ai_data['recommendation']}"
        )

        create_notification(
            db=db,
            title=title,
            message=message,
            severity="Critical",
            sector=sector.name,
        )

        await manager.send_notification(
            title=title,
            message=message,
        )

    # ======================================================
    # CCTV INSIGHT
    # ======================================================

    for alert in ai_data["alerts"]:

        text = alert["message"].lower()

        if (
            "smoke" in text
            or "dense smoke" in text
            or "fire" in text
            or "explosion" in text
            or "gas leak" in text
        ):

            title = "🎥 CCTV INSIGHT"

            message = (
                f"Sector: {sector.name}\n\n"
                f"{alert['message']}"
            )

            create_notification(
                db=db,
                title=title,
                message=message,
                severity="Critical",
                sector=sector.name,
            )

            await manager.send_notification(
                title=title,
                message=message,
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