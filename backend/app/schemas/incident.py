from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ==========================================================
# Create Incident
# ==========================================================

class IncidentCreate(BaseModel):
    sector_id: int
    severity: str
    cause: str
    action: str
    status: str = "Open"


# ==========================================================
# Update Incident
# ==========================================================

class IncidentUpdate(BaseModel):
    severity: Optional[str] = None
    cause: Optional[str] = None
    action: Optional[str] = None
    status: Optional[str] = None


# ==========================================================
# Incident Response
# ==========================================================

class IncidentResponse(BaseModel):
    id: int
    sector_id: int
    severity: str
    cause: str
    action: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================================
# Dashboard Statistics
# ==========================================================

class IncidentStats(BaseModel):
    total_incidents: int
    open_incidents: int
    resolved_incidents: int
    critical_incidents: int