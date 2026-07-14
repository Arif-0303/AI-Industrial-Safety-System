from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.sector import Sector

from app.ai.risk_engine import calculate_risk_score
from app.ai.alert_engine import generate_alerts
from app.ai.predictive_maintenance import predictive_maintenance
from app.ai.incident_prediction import predict_incident

router = APIRouter(
    prefix="/ai",
    tags=["AI Summary"],
)


@router.get("/summary")
def ai_summary(
    db: Session = Depends(get_db),
):
    sectors = db.query(Sector).all()

    total_sectors = len(sectors)
    total_risk = 0
    alerts = []

    critical = 0
    warning = 0
    safe = 0

    maintenance_due = 0

    incidents = []

    for sector in sectors:

        score = calculate_risk_score(sector)
        total_risk += score

        alerts.extend(generate_alerts(sector))

        maintenance = predictive_maintenance(sector)

        if maintenance["maintenance_status"] != "Healthy":
            maintenance_due += 1

        prediction = predict_incident(sector)

        incidents.append(
            {
                "sector": sector.name,
                "probability": prediction["accident_probability"],
                "severity": prediction["severity"],
            }
        )

        if score >= 80:
            critical += 1
        elif score >= 50:
            warning += 1
        else:
            safe += 1

    avg_risk = (
        total_risk / total_sectors
        if total_sectors
        else 0
    )

    return {
        "total_sectors": total_sectors,
        "average_risk": round(avg_risk, 2),
        "critical_sectors": critical,
        "warning_sectors": warning,
        "safe_sectors": safe,
        "maintenance_due": maintenance_due,
        "total_alerts": len(alerts),
        "incident_predictions": incidents,
    }