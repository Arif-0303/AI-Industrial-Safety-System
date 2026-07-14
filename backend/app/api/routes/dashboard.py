from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.sector import Sector

from app.ai.risk_engine import calculate_risk_score

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
):
    sectors = db.query(Sector).all()

    total_sectors = len(sectors)

    high_risk = 0
    active_alerts = 0
    total_workers = 0

    risk_scores = []

    for sector in sectors:
        score = calculate_risk_score(sector)

        risk_scores.append(score)

        if score >= 70:
            high_risk += 1

        if score >= 50:
            active_alerts += 1

        total_workers += sector.workers_present

    avg_risk = (
        sum(risk_scores) / len(risk_scores)
        if risk_scores else 0
    )

    return {
        "total_sectors": total_sectors,
        "high_risk_sectors": high_risk,
        "active_alerts": active_alerts,
        "total_workers": total_workers,
        "average_risk_score": round(avg_risk, 2),
    }