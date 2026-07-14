from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.incident import Incident
from app.schemas.incident import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse,
    IncidentStats,
)

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


# ==========================================================
# Create Incident
# ==========================================================

@router.post("/", response_model=IncidentResponse)
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
):
    new_incident = Incident(
        sector_id=incident.sector_id,
        severity=incident.severity,
        cause=incident.cause,
        action=incident.action,
        status=incident.status,
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    return new_incident


# ==========================================================
# Get All Incidents
# ==========================================================

@router.get("/", response_model=list[IncidentResponse])
def get_incidents(
    status: str | None = Query(default=None),
    severity: str | None = Query(default=None),
    db: Session = Depends(get_db),
):

    query = db.query(Incident)

    if status:
        query = query.filter(Incident.status == status)

    if severity:
        query = query.filter(Incident.severity == severity)

    return query.order_by(
        Incident.created_at.desc()
    ).all()


# ==========================================================
# Get Incident By ID
# ==========================================================

@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):

    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return incident


# ==========================================================
# Update Incident
# ==========================================================

@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    incident: IncidentUpdate,
    db: Session = Depends(get_db),
):

    existing = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    update_data = incident.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing, key, value)

    db.commit()
    db.refresh(existing)

    return existing


# ==========================================================
# Change Status
# ==========================================================

@router.patch("/{incident_id}/status")
def change_status(
    incident_id: int,
    status: str,
    db: Session = Depends(get_db),
):

    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    incident.status = status

    db.commit()

    return {
        "message": "Incident status updated successfully."
    }


# ==========================================================
# Incident Statistics
# ==========================================================

@router.get("/stats/summary", response_model=IncidentStats)
def incident_statistics(
    db: Session = Depends(get_db),
):

    incidents = db.query(Incident).all()

    total = len(incidents)

    open_incidents = len(
        [i for i in incidents if i.status.lower() == "open"]
    )

    resolved = len(
        [i for i in incidents if i.status.lower() == "resolved"]
    )

    critical = len(
        [i for i in incidents if i.severity.lower() == "critical"]
    )

    return IncidentStats(
        total_incidents=total,
        open_incidents=open_incidents,
        resolved_incidents=resolved,
        critical_incidents=critical,
    )


# ==========================================================
# Delete Incident
# ==========================================================

@router.delete("/{incident_id}")
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):

    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    db.delete(incident)
    db.commit()

    return {
        "message": "Incident deleted successfully."
    }