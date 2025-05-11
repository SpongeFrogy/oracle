from typing import Annotated
from pydantic import Field
from pydantic_settings import BaseSettings, ForceDecode

class Settings(BaseSettings):
    RABBITMQ_HOST: str = Field(default='rabbitmq', description='Host for rabbitmq server.')
    RABBITMQ_DEFAULT_USER: str = Field(default="admin", description='Username for RabbitMQ service.') 
    RABBITMQ_DEFAULT_PASS: str = Field(default="secret", description='User password for RabbitMQ service.') 
    RABBITMQ_QUEUE: str = Field(default='signal_queue', description='Rabbitmq queue to listen to.')
    API_BASE_URL: str = Field(default='http://oracle:8000', description='Oracle base URL.')
    
    # connection
    TEST_NET: bool = Field(default=False, description='Do use Hyperliquid-test-net.')

    # donchian settings
    LOOK_BACK_WINDOWS: Annotated[list[int], ForceDecode] = Field(default=[5, 10], description='Look back windows for technical strategy.')
    TARGET_VOLATILITY: float = Field(default=.25, description='Target max drown for the strategy.')
    MAX_ALLOCATION: float = Field(default=1., description='Profile allocate limit.')
    VOLATILITY_WINDOW: int = Field(default=90, description='Window for calculate price volatility.')
    TRADING_DAYS_PER_YEAR: int = Field(default=252, description='Normalize.')
    RISK_FREE_RATE: float = Field(default=.0, description='Normalize.')

    # ml config
    MODELS_DIR: str = Field(default='src/models', description='Directory with model-object files.')
    MODEL_FILE: str = Field(default='combo_clf_prod.joblib', description='File name for model use.')

settings = Settings()
