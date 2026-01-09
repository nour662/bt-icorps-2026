import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    PROJECT_NAME: str = "bt-icorps-2026"
    DEBUG: bool = True

    # DATABASE

    # The types here (str) tell Python how to treat the .env values
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    # DATABASE_URL: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    # AUTHENTICATION / SECURITY
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    JWT_ALGORITHM: str 

    # OPENAI
    OPENAI_API_KEY: str
    
    # OBJECT STORAGE (MINIO/S3)
    S3_ENDPOINT: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str

    # PYDANTIC SETTINGS CONFIG
    model_config = SettingsConfigDict(
                        env_file=".env",
                        extra="ignore"
                    )

# Create a single instance of settings to be used across the app
settings = Settings()