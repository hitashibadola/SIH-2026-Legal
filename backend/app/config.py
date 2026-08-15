import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY: str = os.getenv("LLM_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

def get_api_key(custom_key: Optional[str] = None) -> str:
    """Returns the custom client-provided API key if given, otherwise falls back to the server environment key."""
    key = custom_key.strip() if custom_key and custom_key.strip() else LLM_API_KEY
    if not key:
        raise ValueError("No LLM API key provided. Please provide an API key in the request or set LLM_API_KEY in .env.")
    return key
