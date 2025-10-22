from typing import Literal, List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    ENVIRONMENT: Literal["development", "production"] = "development"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = True

    WHISPER_MODEL_SIZE: Literal["tiny", "base"] = "tiny"
    WHISPER_DEVICE: Literal["cpu", "cuda"] = "cpu"
    ENABLE_AUDIO: bool = True

    MIN_CONFIDENCE_THRESHOLD: float = Field(0.2, ge=0.0, le=1.0)
    MAX_TAGS_PER_TEXT: int = Field(5, ge=1, le=12)
    MAX_TEXT_LENGTH: int = 5000

    DATA_DIR: str = "./data"
    LOG_FILE: str = "./logs/app.log"

    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
