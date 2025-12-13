import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

current_file_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_file_dir))
env_path = os.path.join(backend_dir, ".env")

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Customer Support Copilot"
    API_V1_STR: str = "/api/v1"

    SUPABASE_DB_URL: str
    VECTOR_TABLE_NAME: str = "document_chunks"

    LLM_API_KEY: str
    LLM_MODEL: str = "openai/gpt-oss-120b"

    EMBEDDING_API_KEY: str
    EMBEDDING_MODEL: str
    EMBEDDING_DIMENSION: int = 768

    ADMIN_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=env_path,
        case_sensitive=True,
        extra="ignore"
    )

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()