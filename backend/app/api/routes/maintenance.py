from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.maintenance import Maintenance
from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceResponse,
)

router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"],
)


@router.post("/", response_model=MaintenanceResponse)
def create_maintenance(
    maintenance: MaintenanceCreate,
    db: Session = Depends(get_db),
):
    new_record = Maintenance(**maintenance.model_dump())

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


@router.get("/", response_model=list[MaintenanceResponse])
def get_maintenance_records(
    db: Session = Depends(get_db),
):
    return db.query(Maintenance).all()


@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
def get_maintenance_record(
    maintenance_id: int,
    db: Session = Depends(get_db),
):
    record = (
        db.query(Maintenance)
        .filter(Maintenance.id == maintenance_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found",
        )

    return record


@router.put("/{maintenance_id}", response_model=MaintenanceResponse)
def update_maintenance(
    maintenance_id: int,
    maintenance: MaintenanceCreate,
    db: Session = Depends(get_db),
):
    record = (
        db.query(Maintenance)
        .filter(Maintenance.id == maintenance_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found",
        )

    for key, value in maintenance.model_dump().items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record


@router.delete("/{maintenance_id}")
def delete_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
):
    record = (
        db.query(Maintenance)
        .filter(Maintenance.id == maintenance_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found",
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Maintenance record deleted successfully"
    }