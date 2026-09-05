from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    gemini_embedding_model: str = "text-embedding-004"
    supabase_url: str = ""
    supabase_key: str = ""
    admin_api_key: str = ""
    max_file_size_mb: int = 20
    max_url_length: int = 2048
    cors_origins: str = "http://localhost:3000"
    retrieval_relevance_threshold: float = .45
    request_timeout_seconds: float = 15
    min_web_text_characters: int = 300
    @property
    def cors_origin_list(self): return [x.strip() for x in self.cors_origins.split(',') if x.strip()]

@lru_cache
def get_settings() -> Settings: return Settings()
