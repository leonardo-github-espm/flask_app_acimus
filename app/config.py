import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookies/session
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("FLASK_ENV") == "production"

    # CSRF
    WTF_CSRF_ENABLED = True

    # Limiter
    RATELIMIT_DEFAULT = "200 per minute"
    ENV = os.getenv("FLASK_ENV", "development")

