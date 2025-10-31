from pydantic import BaseSettings

class Settings(BaseSettings):
    OPEN_API_KEY: str
    MODEL: str = "gpt-4o-mini"
    AGENT_BASE_URL: str = "https://agent-domain.com"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()