from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):

    ############################################
    # Application
    ############################################

    APP_NAME: str = "AI Job Search Assistant"
    APP_ENV: str = "development"
    APP_URL: str

    ############################################
    # Security
    ############################################

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ############################################
    # Database
    ############################################

    DATABASE_URL: str

    ############################################
    # Redis
    ############################################

    REDIS_URL: str

    ############################################
    # Google OAuth
    ############################################

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    GOOGLE_OAUTH_STATE_EXPIRE_SECONDS: int = 600

    ############################################
    # Gmail
    ############################################

    GMAIL_SCOPES: str = (
        "openid "
        "https://www.googleapis.com/auth/userinfo.email "
        "https://www.googleapis.com/auth/userinfo.profile "
        "https://www.googleapis.com/auth/gmail.readonly"
    )

    ############################################
    # AI
    ############################################

    AI_BASE_URL: str = "https://api.openai.com/v1"

    AI_API_KEY: str = ""

    AI_MODEL: str = "gpt-5"

    AI_TIMEOUT: int = 120

    ############################################
    # Logging
    ############################################

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
