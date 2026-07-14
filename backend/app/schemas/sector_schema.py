from pydantic import BaseModel


class Sector(BaseModel):
    id: int
    name: str
    temperature: int
    gas: int
    pressure: float
    workers: int
    maintenance: str
    risk: str