"""Transaction schemas."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TransactionType(str, Enum):
    """Transaction types."""

    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    SIGNAL_PURCHASE = "SIGNAL_PURCHASE"


class TransactionStatus(str, Enum):
    """Transaction statuses."""

    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TransactionBase(BaseModel):
    """Base transaction schema."""

    amount: float = Field(..., gt=0, description="Transaction amount in Tugrik")
    type: TransactionType = Field(..., description="Type of transaction")
    description: Optional[str] = Field(None, description="Transaction description")


class TransactionCreate(TransactionBase):
    """Transaction creation schema."""

    pass


class TransactionResponse(TransactionBase):
    """Transaction response schema."""

    id: int = Field(..., description="Transaction ID")
    user_id: int = Field(..., description="User ID")
    status: TransactionStatus = Field(..., description="Transaction status")
    created_at: datetime = Field(..., description="Transaction creation timestamp")
    updated_at: datetime = Field(..., description="Transaction last update timestamp")

    class Config:
        """Pydantic config."""

        from_attributes = True
