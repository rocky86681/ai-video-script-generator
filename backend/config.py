"""
Configuration module for the AI Video Script Generator backend.
Loads environment variables and provides app-wide settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Get the directory where config.py is located
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file inside the backend directory
load_dotenv(dotenv_path=BASE_DIR / ".env")


class Settings:
    """Application settings loaded from environment variables."""

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # CORS origins allowed to access the API
    CORS_ORIGINS: list = [
        "http://localhost:5173",   # Vite dev server
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:3000",   # Alternate React dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:3000",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ]

    # API metadata
    APP_TITLE: str = "AI Video Script Generator API"
    APP_DESCRIPTION: str = (
        "Generate professional video scripts using AI. "
        "Supports YouTube, Cinematic, and Instagram Reel styles."
    )
    APP_VERSION: str = "1.0.0"


settings = Settings()
