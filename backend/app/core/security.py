from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets
import hashlib
import uuid

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)

# ==========================================================
# Password Hashing
# ==========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ==========================================================
# Password Functions
# ==========================================================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ==========================================================
# Access Token
# ==========================================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "access",
            "jti": str(uuid.uuid4()),
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ==========================================================
# Refresh Token
# ==========================================================

def create_refresh_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=REFRESH_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "refresh",
            "jti": str(uuid.uuid4()),
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ==========================================================
# Verify JWT
# ==========================================================

def verify_access_token(token: str) -> Optional[dict]:

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return payload

    except JWTError:
        return None


# ==========================================================
# Verify Refresh Token
# ==========================================================

def verify_refresh_token(token: str):

    payload = verify_access_token(token)

    if payload is None:
        return None

    if payload.get("type") != "refresh":
        return None

    return payload


# ==========================================================
# Password Reset Token
# ==========================================================

def generate_reset_token() -> str:
    """
    Secure random token sent to user.
    """
    return secrets.token_urlsafe(48)


# ==========================================================
# Hash Reset Token
# ==========================================================

def hash_reset_token(token: str) -> str:
    """
    Store only hashed reset token.
    """
    return hashlib.sha256(
        token.encode()
    ).hexdigest()


# ==========================================================
# Verify Reset Token
# ==========================================================

def verify_reset_token(
    plain_token: str,
    hashed_token: str,
) -> bool:

    return (
        hashlib.sha256(
            plain_token.encode()
        ).hexdigest()
        == hashed_token
    )


# ==========================================================
# Token Expiry
# ==========================================================

def get_reset_token_expiry():

    return datetime.utcnow() + timedelta(
        minutes=30
    )