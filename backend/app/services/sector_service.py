from sqlalchemy.orm import Session

from app.models.sector import Sector

from app.ai.alert_engine import generate_alerts
from app.ai.predictive_maintenance import predictive_maintenance
from app.ai.incident_prediction import predict_incident
from app.ai.risk_engine import calculate_risk_score
from app.ai.risk_label import risk_label
from app.ai.recommendation_engine import recommendation


def get_all_sectors(db: Session):

    sectors = db.query(Sector).all()

    response = []

    for sector in sectors:

        score = calculate_risk_score(sector)
        prediction = predictive_maintenance(sector)
        incident = predict_incident(sector)

        response.append({

            "id": sector.id,
            "name": sector.name,
            "temperature": sector.temperature,
            "gas": sector.gas,
            "pressure": sector.pressure,
            "workers_present": sector.workers_present,
            "maintenance": sector.maintenance,
            "risk": sector.risk,

            "risk_score": score,
            "risk_level": risk_label(score),
            "recommendation": recommendation(score),
            "alerts": generate_alerts(sector),

            "machine_health": prediction["machine_health"],
            "remaining_life": prediction["remaining_life"],
            "maintenance_status": prediction["maintenance_status"],

            "accident_probability": incident["probability"],
            "incident_type": incident["incident"],
            "incident_severity": incident["severity"],
            "incident_confidence": incident["confidence"],
            "estimated_time": incident["estimated_time"],
            "incident_cause": incident["reason"],
            "incident_recommendation": incident["recommendation"],
        })

    return response