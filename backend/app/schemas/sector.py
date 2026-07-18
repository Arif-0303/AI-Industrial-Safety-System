from typing import Any
from pydantic import BaseModel


class SectorResponse(BaseModel):
    id: int
    name: str
    temperature: float
    gas: float
    pressure: float
    workers_present: int
    maintenance: str
    risk: str

    # AI Risk
    risk_score: int
    risk_level: str
    recommendation: str

    # generate_alerts() returns a DICTIONARY
    alerts: dict[str, Any]

    # Predictive Maintenance
    machine_health: int
    remaining_life: int
    maintenance_status: str

    # Incident Prediction
    accident_probability: int
    incident_severity: str
    incident_cause: str
    incident_recommendation: str

    class Config:
        from_attributes = True