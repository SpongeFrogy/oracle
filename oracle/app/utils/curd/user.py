from typing import Optional
from sqlalchemy.orm import Session
from app.db.models import User

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)

def get_user(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()