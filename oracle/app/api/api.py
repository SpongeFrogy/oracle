from fastapi import APIRouter

from app.api.endpoints import auth, users, transactions, signals

api_router = APIRouter()

api_router.include_router(auth.router, prefix='/auth', tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(transactions.router, prefix='/transactions', tags=['transactions'])
api_router.include_router(signals.router, prefix='/signals', tags=['signals'])
