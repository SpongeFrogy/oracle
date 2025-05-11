"""Transaction endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import Transaction, User
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionType,
    TransactionStatus,
)

router = APIRouter()


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionResponse:
    """
    Create a new transaction.

    Args:
        transaction: Transaction data
        db: Database session
        current_user: Current authenticated user

    Returns:
        TransactionResponse: Created transaction

    Raises:
        HTTPException: If transaction creation fails
    """
    # Create transaction
    db_transaction = Transaction(
        user_id=current_user.id,
        amount=transaction.amount,
        type=transaction.type,
        status=TransactionStatus.PENDING,
        description=transaction.description,
    )
    db.add(db_transaction)

    try:
        # Update user balance based on transaction type
        if transaction.type == TransactionType.DEPOSIT:
            current_user.tugrik_balance += transaction.amount
        elif transaction.type == TransactionType.WITHDRAWAL:
            if current_user.tugrik_balance < transaction.amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient balance",
                )
            current_user.tugrik_balance -= transaction.amount
        elif transaction.type == TransactionType.SIGNAL_PURCHASE:
            if current_user.tugrik_balance < transaction.amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient balance for signal purchase",
                )
            current_user.tugrik_balance -= transaction.amount

        db_transaction.status = TransactionStatus.COMPLETED
        db.commit()
        db.refresh(db_transaction)

        return TransactionResponse.from_orm(db_transaction)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[TransactionResponse]:
    """
    Get user's transaction history.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Current authenticated user

    Returns:
        List[TransactionResponse]: List of transactions
    """
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()
    return [TransactionResponse.from_orm(t) for t in transactions]


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionResponse:
    """
    Get a specific transaction.

    Args:
        transaction_id: ID of the transaction
        db: Database session
        current_user: Current authenticated user

    Returns:
        TransactionResponse: Transaction details

    Raises:
        HTTPException: If transaction not found or not owned by user
    """
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id,
        )
        .first()
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    return TransactionResponse.from_orm(transaction)
