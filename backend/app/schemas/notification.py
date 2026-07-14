from datetime import datetime
from pydantic import BaseModel, Field


# ==========================================
# Create Notification
# ==========================================

class NotificationCreate(BaseModel):
    title: str = Field(..., max_length=255)
    message: str = Field(..., max_length=1000)
    notification_type: str = "Info"
    priority: str = "Low"


# ==========================================
# Update Notification
# ==========================================

class NotificationUpdate(BaseModel):
    is_read: bool


# ==========================================
# Notification Response
# ==========================================

class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    notification_type: str
    priority: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True