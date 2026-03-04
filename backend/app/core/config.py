from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "YouTube Analysis API"
    API_V1_STR: str = "/api/v1"
    YOUTUBE_API_KEY: str = "" # To be provided in .env

    class Config:
        env_file = ".env"

settings = Settings()
