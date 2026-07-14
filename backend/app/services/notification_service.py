from sqlalchemy.orm import Session
import asyncio

from app.models.notification import Notification
from app.websocket.connection_manager import manager


def create_notification(
    db: Session,
    title: str,
    message: str,
    severity: str,
    sector: str,
):
    notification = Notification(
        title=title,
        message=message,
        severity=severity,
        sector=sector,
        is_read=False,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    # ==========================================
    # Broadcast notification to all dashboards
    # ==========================================

    try:
        asyncio.create_task(
            manager.send_notification(
                title=title,
                message=message,
            )
        )
    except RuntimeError:
        pass

    return notification


def get_notifications(db: Session):
    return (
        db.query(Notification)
        .order_by(Notification.created_at.desc())
        .all()
    )


def mark_as_read(
    db: Session,
    notification_id: int,
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if notification is None:
        return None

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification


def delete_notification(
    db: Session,
    notification_id: int,
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if notification is None:
        return None

    db.delete(notification)
    db.commit()

    return notification


def unread_notification_count(db: Session):
    return (
        db.query(Notification)
        .filter(Notification.is_read == False)
        .count()
    )