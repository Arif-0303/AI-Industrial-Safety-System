from pydantic import BaseModel


class Alert(BaseModel):
    type: str
    message: str