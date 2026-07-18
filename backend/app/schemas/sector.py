from pydantic import BaseModel
from typing import Dict, Any


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

    # Your generate_alerts() returns a dictionary, not a list
    alerts: Dict[str, Any]

    # Predictive Maintenance
    machine_health: int
    remaining_life: int
    maintenance_status: str

    # Incident Prediction
    accident_probability: int
    incident_type: str
    incident_severity: str
    incident_confidence: str
    estimated_time: str
    incident_cause: str
    incident_recommendation: str

    class Config:
        from_attributes = True