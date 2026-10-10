import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="allow",
        case_sensitive=True
    )

    PROJECT_NAME: str = "ContractMind"
    VERSION: str = "1.5.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = Field(default="contractmind_super_secret_jwt_key_change_in_production_2026", validation_alias="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./contractmind.db", validation_alias="DATABASE_URL")
    
    # Vector DB
    CHROMA_PERSIST_DIR: str = Field(default="./chroma_data", validation_alias="CHROMA_PERSIST_DIR")
    
    # LLM Providers
    OPENAI_API_KEY: str = Field(default="", validation_alias="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = Field(default="", validation_alias="ANTHROPIC_API_KEY")
    GEMINI_API_KEY: str = Field(default="", validation_alias="GEMINI_API_KEY")
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434", validation_alias="OLLAMA_BASE_URL")
    DEFAULT_MODEL: str = Field(default="gemini-3.5-flash-lite", validation_alias="DEFAULT_MODEL")
    FALLBACK_MODEL: str = Field(default="deepseek-r1:latest", validation_alias="FALLBACK_MODEL")
    
    # Storage
    UPLOAD_DIR: str = Field(default="./uploads", validation_alias="UPLOAD_DIR")
    EXPORT_DIR: str = Field(default="./exports", validation_alias="EXPORT_DIR")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]


settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.EXPORT_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
