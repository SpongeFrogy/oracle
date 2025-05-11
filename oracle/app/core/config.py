from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application."""

    # Application
    APP_NAME: str = "Oracle"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api"

    # Security
    SECRET_KEY: str = "bla-bla-bla-blu-blu-blu"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    POSTGRES_SERVER: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "oracle_db"

    # Redis
    # REDIS_HOST: str = "localhost"
    # REDIS_PORT: int = 6379
    # REDIS_DB: int = 0

    # RabbitMQ
    # RABBITMQ_HOST: str = "localhost"
    # RABBITMQ_PORT: int = 5672
    # RABBITMQ_USER: str = "guest"
    # RABBITMQ_PASSWORD: str = "guest"

    # ML Service
    # MODEL_PATH: str = "app/ml/models"
    # CACHE_EXPIRATION: int = 600  # 10 minutes in seconds

    # Monitoring
    # PROMETHEUS_MULTIPROC_DIR: str = "/tmp"

    class Config:
        """Configuration for the application."""

        env_file = ".env"


settings = Settings()
