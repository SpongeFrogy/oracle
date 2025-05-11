from pydantic import BaseModel

class Prediction(BaseModel):
    confidence: float
    timestamp: int