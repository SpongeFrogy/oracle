from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from .prediction import Prediction

class Suggestion(str, Enum):
    BUY = 'BUY'
    HOLD = 'HOLD'
    SHORT = 'SHORT'

class SignalType(str, Enum):
    TECHNICAL = "TECHNICAL"
    ML = "ML"

class SignalRequest(BaseModel):
    symbol: str
    signal_type: SignalType

class SignalResponse(BaseModel):
    success: bool
    suggestion: Suggestion
    timestamp: int
    prediction: Optional[Prediction] = Field(default=None, description="ML prediction if enabled.")