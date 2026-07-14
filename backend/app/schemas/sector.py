from pydantic import BaseModel
from app.schemas.alert import Alert


class SectorResponse(BaseModel):
    id: int
    name: str
    temperature: float
    gas: float
    pressure: float
    workers_present: int
    maintenance: str
    risk: str

    # AI Risk Fields
    risk_score: int
    risk_level: str
    recommendation: str
    alerts: list[Alert]

    # Predictive Maintenance Fields
    machine_health: int
    remaining_life: int
    maintenance_status: str
    accident_probability: int
    incident_severity: str
    incident_cause: str
    incident_recommendation: str

    class Config:
        from_attributes = True