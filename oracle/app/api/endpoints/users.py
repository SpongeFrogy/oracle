from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.utils.curd.user import create_user
router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_current_user(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get current user."""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_user(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    user_in: UserUpdate,
) -> Any:
    """Update current user."""
    if user_in.email is not None:
        if db.query(User).filter(User.email == user_in.email).filter(User.id != current_user.id).first():
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )
        current_user.email = user_in.email

    if user_in.username is not None:
        if db.query(User).filter(User.username == user_in.username).filter(User.id != current_user.id).first():
            raise HTTPException(
                status_code=400,
                detail="Username already registered",
            )
        current_user.username = user_in.username

    create_user(db, current_user)
    return current_user
