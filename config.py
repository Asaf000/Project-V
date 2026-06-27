"""
------------------------------------------------------------
Project : E-Commerce Web Application
Configuration File
Author : Thinkora Labs
------------------------------------------------------------
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# ----------------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------------

load_dotenv()


class Config:
    """
    Base Configuration Class
    """

    # ------------------------------------------------------
    # Flask Configuration
    # ------------------------------------------------------

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "this-is-a-development-secret-key"
    )

    DEBUG = True

    TESTING = False

    # ------------------------------------------------------
    # Database Configuration
    # ------------------------------------------------------

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost/ecommerce_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    # ------------------------------------------------------
    # Upload Configuration
    # ------------------------------------------------------

    UPLOAD_FOLDER = os.path.join(
        "static",
        "uploads"
    )

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "webp"
    }

    # ------------------------------------------------------
    # Session Configuration
    # ------------------------------------------------------

    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    # Change to True in Production (HTTPS)
    SESSION_COOKIE_SECURE = False

    # ------------------------------------------------------
    # Remember Me Cookie
    # ------------------------------------------------------

    REMEMBER_COOKIE_DURATION = timedelta(days=7)

    REMEMBER_COOKIE_HTTPONLY = True

    REMEMBER_COOKIE_SECURE = False

    # ------------------------------------------------------
    # CSRF Protection
    # ------------------------------------------------------

    WTF_CSRF_ENABLED = True

    WTF_CSRF_TIME_LIMIT = None

    # ------------------------------------------------------
    # Pagination
    # ------------------------------------------------------

    PRODUCTS_PER_PAGE = 12

    ORDERS_PER_PAGE = 10

    # ------------------------------------------------------
    # Default Admin
    # ------------------------------------------------------

    DEFAULT_ADMIN_EMAIL = "admin@gmail.com"

    DEFAULT_ADMIN_PASSWORD = "admin123"

    # ------------------------------------------------------
    # Application Details
    # ------------------------------------------------------

    APP_NAME = "E-Commerce Web Application"

    APP_VERSION = "1.0.0"

    COMPANY = "Thinkora Labs"

    # ------------------------------------------------------
    # Order Status
    # ------------------------------------------------------

    ORDER_STATUS = [
        "Pending",
        "Confirmed",
        "Packed",
        "Shipped",
        "Out for Delivery",
        "Delivered",
        "Cancelled"
    ]


# ----------------------------------------------------------
# Development Configuration
# ----------------------------------------------------------

class DevelopmentConfig(Config):

    DEBUG = True


# ----------------------------------------------------------
# Production Configuration
# ----------------------------------------------------------

class ProductionConfig(Config):

    DEBUG = False

    SESSION_COOKIE_SECURE = True

    REMEMBER_COOKIE_SECURE = True


# ----------------------------------------------------------
# Testing Configuration
# ----------------------------------------------------------

class TestingConfig(Config):

    TESTING = True

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///:memory:"
    )


# ----------------------------------------------------------
# Configuration Dictionary
# ----------------------------------------------------------

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
