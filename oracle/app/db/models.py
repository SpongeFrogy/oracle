from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship
from app.db.session import Base, engine


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    tugrik_balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="user")
    signals = relationship("Signal", back_populates="user")

class Transaction(Base):
    """Transaction model."""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(
        Enum("DEPOSIT", "WITHDRAWAL", "SIGNAL_PURCHASE", name="transaction_type"),
        nullable=False,
    )
    status = Column(
        Enum("PENDING", "COMPLETED", "FAILED", name="transaction_status"),
        nullable=False,
    )
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="transactions")

class Signal(Base):
    __tablename__ = "signals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, nullable=False)
    signal_type = Column(
        Enum("TECHNICAL", "ML", name='signal_type'),
        nullable=False
    )
    status = Column(
        Enum("PROCESSING", "COMPLETED", "FAILED", name='signal_status'),
        nullable=False
    )
    suggestion = Column(
        Enum("BUY", "HOLD", "SHORT", name='suggestion'), nullable=True
    )
    cost = Column(Float, nullable=False)

    user = relationship("User", back_populates="signals")

Base.metadata.create_all(engine)