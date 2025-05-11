from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    username: str
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""

    id: int
    tugrik_balance: float
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True