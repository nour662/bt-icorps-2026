import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "bt-icorps-2026"
    DEBUG: bool = True

    # The types here (str) tell Python how to treat the .env values
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    # DATABASE_URL: str
    DB_HOST: str = "localhost"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgressql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"


    OPENAI_API_KEY: str
    
    S3_ENDPOINT: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str

    # This line tells Pydantic to look for the .env file
    model_config = SettingsConfigDict(
                        env_file=".env",
                        extra="ignore"
                    )

# Create a single instance of settings to be used across the app
settings = Settings()