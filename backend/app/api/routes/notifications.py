from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.notification import Notification
from app.services.notification_service import (
    get_notifications,
    mark_as_read,
    delete_notification,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get("/")
def all_notifications(
    db: Session = Depends(get_db),
):
    notifications = get_notifications(db)

    return {
        "success": True,
        "count": len(notifications),
        "data": notifications,
    }


@router.put("/{notification_id}/read")
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    notification = mark_as_read(
        db,
        notification_id,
    )

    if notification is None:
        return {
            "success": False,
            "message": "Notification not found",
        }

    return {
        "success": True,
        "message": "Notification marked as read.",
    }


@router.delete("/{notification_id}")
def remove_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    notification = delete_notification(
        db,
        notification_id,
    )

    if notification is None:
        return {
            "success": False,
            "message": "Notification not found",
        }

    return {
        "success": True,
        "message": "Notification deleted.",
    }