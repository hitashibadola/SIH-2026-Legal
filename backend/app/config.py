"""Compatibility import; new configuration lives in app.core.config."""
from app.core.config import Settings, get_settings

settings = get_settings()
