from datetime import timedelta
import os

# ==========================================================
# Application
# ==========================================================

APP_NAME = "AI Industrial Safety Monitoring System"

APP_VERSION = "1.0.0"

DEBUG = True

# ==========================================================
# JWT Configuration
# ==========================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "CHANGE_THIS_TO_A_RANDOM_64_CHARACTER_SECRET_KEY"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

REFRESH_TOKEN_EXPIRE_DAYS = 7

REFRESH_TOKEN_EXPIRE = timedelta(
    days=REFRESH_TOKEN_EXPIRE_DAYS
)

REFRESH_TOKEN_EXPIRE_MINUTES = (
    REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60
)

# ==========================================================
# Password Reset
# ==========================================================

RESET_PASSWORD_TOKEN_EXPIRE_MINUTES = 30

# ==========================================================
# Frontend URL
# ==========================================================

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

# ==========================================================
# Email Configuration
# ==========================================================

MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")

MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")

MAIL_FROM = os.getenv(
    "MAIL_FROM",
    "noreply@industrialsafety.ai"
)

MAIL_SERVER = os.getenv(
    "MAIL_SERVER",
    "smtp.gmail.com"
)

MAIL_PORT = int(
    os.getenv("MAIL_PORT", 587)
)

MAIL_STARTTLS = True

MAIL_SSL_TLS = False

# ==========================================================
# Security
# ==========================================================

MAX_LOGIN_ATTEMPTS = 5

ACCOUNT_LOCK_MINUTES = 15

PASSWORD_MIN_LENGTH = 6

PASSWORD_RESET_URL = (
    f"{FRONTEND_URL}/reset-password"
)

# ==========================================================
# Future Production Config
# ==========================================================

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379"
)

POSTGRES_URL = os.getenv(
    "POSTGRES_URL",
    ""
)

MQTT_BROKER = os.getenv(
    "MQTT_BROKER",
    ""
)

MQTT_PORT = int(
    os.getenv("MQTT_PORT", 1883)
)

# ==========================================================
# AI Configuration
# ==========================================================

MODEL_NAME = "Industrial Safety AI"

MODEL_VERSION = "1.0"

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = "INFO"