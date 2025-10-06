from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    gomarket_api_key: str = Field(..., env="GOMARKET_API_KEY")
    mock: bool = Field(True, env="MOCK")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"

settings = Settings()