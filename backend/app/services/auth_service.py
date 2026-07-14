from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.config import MAX_LOGIN_ATTEMPTS, ACCOUNT_LOCK_MINUTES
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
)


def authenticate_user(
    email: str,
    password: str,
    db: Session,
):
    """
    Authenticate user and return JWT tokens.
    """

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    # Invalid Email
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Account Disabled
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been deactivated.",
        )

    # Unlock account automatically if lock time has expired
    if (
        user.account_locked
        and user.account_locked_until
        and user.account_locked_until <= datetime.utcnow()
    ):
        user.account_locked = False
        user.account_locked_until = None
        user.failed_login_attempts = 0
        db.commit()
        db.refresh(user)

    # Account Locked
    if user.account_locked:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Account is temporarily locked due to multiple failed login attempts.",
        )

    # Wrong Password
    if not verify_password(password, user.password):

        user.failed_login_attempts += 1

        if user.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
            user.account_locked = True
            user.account_locked_until = (
                datetime.utcnow()
                + timedelta(minutes=ACCOUNT_LOCK_MINUTES)
            )

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Successful Login

    user.failed_login_attempts = 0
    user.account_locked = False
    user.account_locked_until = None
    user.last_login = datetime.utcnow()

    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        {
            "sub": user.email,
            "role": user.role,
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": user.email,
            "role": user.role,
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
    }