from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "AI Job Search Assistant"

    DATABASE_URL: str

    REDIS_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
