import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    PROJECT_NAME: str = "ContractMind v1.5"
    VERSION: str = "1.5.3"
    API_V1_STR: str = "/api/v1"

    # Runtime Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    IS_VERCEL: bool = os.getenv("VERCEL") == "1"

    # API Keys & LLM endpoints
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Storage Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    @property
    def DATA_DIR(self) -> Path:
        if self.IS_VERCEL:
            return Path("/tmp/data")
        path = self.BASE_DIR / "data"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def UPLOAD_DIR(self) -> Path:
        if self.IS_VERCEL:
            return Path("/tmp/uploads")
        path = self.DATA_DIR / "uploads"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def EXPORT_DIR(self) -> Path:
        if self.IS_VERCEL:
            return Path("/tmp/exports")
        path = self.DATA_DIR / "exports"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def CHROMA_PERSIST_DIR(self) -> Path:
        if self.IS_VERCEL:
            return Path("/tmp/chromadb")
        path = self.DATA_DIR / "chromadb"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def SQLITE_DB_PATH(self) -> Path:
        if self.IS_VERCEL:
            return Path("/tmp/contractmind.db")
        return self.DATA_DIR / "contractmind.db"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        db_path = str(self.SQLITE_DB_PATH).replace("\\", "/")
        return f"sqlite+aiosqlite:///{db_path}"


settings = Settings()
