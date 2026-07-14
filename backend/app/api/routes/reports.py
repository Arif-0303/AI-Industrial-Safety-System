from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.sector import Sector

from app.ai.risk_engine import calculate_risk_score
from app.ai.recommendation_engine import recommendation
from app.ai.alert_engine import generate_alerts

from app.services.report_service import generate_pdf_report

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/")
def get_reports(
    db: Session = Depends(get_db),
):
    sectors = db.query(Sector).all()

    reports = []

    for sector in sectors:
        score = calculate_risk_score(sector)

        reports.append(
            {
                "sector": sector.name,
                "risk_score": score,
                "recommendation": recommendation(score),
                "alerts": generate_alerts(sector),
            }
        )

    return reports


@router.get("/pdf")
def download_pdf_report(
    db: Session = Depends(get_db),
):
    sectors = db.query(Sector).all()

    filename = generate_pdf_report(sectors)

    return FileResponse(
        path=filename,
        filename="Industrial_Safety_Report.pdf",
        media_type="application/pdf",
    )