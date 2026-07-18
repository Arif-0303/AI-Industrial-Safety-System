from sqlalchemy.orm import Session
from sqlalchemy import and_
import asyncio

from app.models.notification import Notification
from app.websocket.connection_manager import manager


# ==========================================================
# CREATE OR UPDATE NOTIFICATION
# ==========================================================

def upsert_notification(
    db: Session,
    title: str,
    message: str,
    severity: str,
    sector: str,
):

    notification = (
        db.query(Notification)
        .filter(
            and_(
                Notification.title == title,
                Notification.sector == sector,
            )
        )
        .first()
    )

    # ---------------- UPDATE ----------------

    if notification:

        changed = (
            notification.message != message
            or notification.severity != severity
        )

        notification.message = message
        notification.severity = severity
        notification.is_read = False

        db.commit()
        db.refresh(notification)

        # Broadcast ONLY if something actually changed
        if changed:
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

    # ---------------- CREATE ----------------

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


# ==========================================================
# DELETE NOTIFICATION
# ==========================================================

def delete_sector_notification(
    db: Session,
    title: str,
    sector: str,
):

    notification = (
        db.query(Notification)
        .filter(
            and_(
                Notification.title == title,
                Notification.sector == sector,
            )
        )
        .first()
    )

    if notification:

        db.delete(notification)
        db.commit()


# ==========================================================
# GET NOTIFICATIONS
# ==========================================================

def get_notifications(db: Session):

    return (
        db.query(Notification)
        .order_by(Notification.created_at.desc())
        .all()
    )


# ==========================================================
# MARK AS READ
# ==========================================================

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


# ==========================================================
# DELETE BY ID
# ==========================================================

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


# ==========================================================
# UNREAD COUNT
# ==========================================================

def unread_notification_count(db: Session):

    return (
        db.query(Notification)
        .filter(Notification.is_read == False)
        .count()
    )