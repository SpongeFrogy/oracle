from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user, get_db
from app.db.models import Transaction, User, Signal
from app.schemas.signal import SignalRequest, SignalResponse, InfernoResponse, SignalStatus
from app.schemas.transaction import TransactionStatus
from app.services.signal import SignalHandler
from datetime import datetime

router = APIRouter()


@router.post("/for_money_yes", response_model=SignalResponse)
async def for_money_yes(
    signal_request: SignalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cost = 10. if signal_request.signal_type == "ML" else 5.

    if current_user.tugrik_balance < cost: # type: ignore
        raise HTTPException(status_code=400, detail="Insufficient funds")

    signal_rpc = SignalHandler()

    payload = signal_request.model_dump()

    db_signal = Signal(
        user_id=current_user.id,
        symbol=signal_request.symbol,
        signal_type=signal_request.signal_type,
        status=SignalStatus.PROCESSING,
        suggestion=None,
        cost=cost,
    )
    db.add(db_signal)
    inferno_response = InfernoResponse(**signal_rpc.call(payload))
    if inferno_response.success:
        db_signal.status = SignalStatus.COMPLETED
        db_signal.suggestion = inferno_response.suggestion
    else:
        db_signal.status = SignalStatus.FAILED
    db.commit()
    db.refresh(db_signal)

    db_transaction = Transaction(
        user_id=current_user.id,
        amount=cost,
        type="SIGNAL_PURCHASE",
        status=TransactionStatus.PENDING,
        description="",
    )
    db.add(db_transaction)
    current_user.tugrik_balance -= cost # type: ignore
    db_transaction.status = TransactionStatus.COMPLETED # type: ignore
    db.commit()
    db.refresh(db_transaction)


    return SignalResponse(
        id=db_signal.id,
        symbol=signal_request.symbol,
        signal_type=signal_request.signal_type,
        status=db_signal.status,
        response=inferno_response,
        cost=cost
    )