import os

class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY", "")
    TOMTOM_BASE_URL = os.getenv("TOMTOM_BASE_URL", "https://api.tomtom.com")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@db:5432/geosense"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ROUTING_CACHE_TTL_SECONDS = int(os.getenv("ROUTING_CACHE_TTL_SECONDS", "30"))
