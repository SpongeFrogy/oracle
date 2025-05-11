from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class SignalType(str, Enum):
    TECHNICAL = "TECHNICAL"
    ML = "ML"

class Suggestion(str, Enum):
    BUY = 'BUY'
    HOLD = 'HOLD'
    SHORT = 'SHORT'

class SignalStatus(str, Enum):
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class SignalRequest(BaseModel):
    symbol: str
    signal_type: SignalType

class Prediction(BaseModel):
    confidence: float
    timestamp: int

class InfernoResponse(BaseModel):
    success: bool
    suggestion: Suggestion
    timestamp: int
    prediction: Optional[Prediction] = None

class SignalResponse(SignalRequest):
    id: int
    status: SignalStatus
    response: InfernoResponse
    cost: float