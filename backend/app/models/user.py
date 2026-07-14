from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from datetime import datetime

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    # ==========================================
    # Primary Key
    # ==========================================
    id = Column(Integer, primary_key=True, index=True)

    # ==========================================
    # Personal Information
    # ==========================================
    name = Column(String(100), nullable=False)

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    # ==========================================
    # Authentication
    # ==========================================
    password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(50),
        nullable=False,
        default="worker"
    )

    # ==========================================
    # Account Status
    # ==========================================
    is_active = Column(
        Boolean,
        default=True
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    # ==========================================
    # Password Reset
    # ==========================================
    reset_token = Column(
        String(255),
        nullable=True
    )

    reset_token_expiry = Column(
        DateTime,
        nullable=True
    )

    # ==========================================
    # Future Ready Fields
    # ==========================================
    last_login = Column(
        DateTime,
        nullable=True
    )

    failed_login_attempts = Column(
        Integer,
        default=0
    )

    account_locked = Column(
        Boolean,
        default=False
    )

    account_locked_until = Column(
        DateTime,
        nullable=True
    )

    # ==========================================
    # Audit
    # ==========================================
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )