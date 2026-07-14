from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.user import User
from app.models.sector import Sector
from app.models.sensor_data import SensorData
from app.models.incident import Incident
from app.models.maintenance import Maintenance

from app.ai.risk_engine import calculate_risk_score

router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"],
)


@router.get("/analytics")
def admin_dashboard(
    db: Session = Depends(get_db),
):

    users = db.query(User).all()
    sectors = db.query(Sector).all()
    incidents = db.query(Incident).all()
    maintenance = db.query(Maintenance).all()
    sensor_history = db.query(SensorData).all()

    total_workers = sum(
        sector.workers_present
        for sector in sectors
    )

    average_risk = 0

    if sectors:
        average_risk = sum(
            calculate_risk_score(sector)
            for sector in sectors
        ) / len(sectors)

    high_risk = len(
        [
            sector
            for sector in sectors
            if calculate_risk_score(sector) >= 70
        ]
    )

    return {
        "total_users": len(users),
        "total_sectors": len(sectors),
        "total_workers": total_workers,
        "total_sensor_records": len(sensor_history),
        "total_incidents": len(incidents),
        "total_maintenance_records": len(maintenance),
        "high_risk_sectors": high_risk,
        "average_risk_score": round(
            average_risk,
            2,
        ),
    }