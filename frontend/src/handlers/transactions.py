import streamlit as st
import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class TransactionType(str, Enum):
    """Transaction types."""

    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    SIGNAL_PURCHASE = "SIGNAL_PURCHASE"

class TransactionCreate(BaseModel):
    amount: float
    type: TransactionType  # "deposit", "withdrawal", "signal_purchase"
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    status: str
    created_at: datetime
    description: Optional[str] = None

class TransactionsHandler:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url

    def create_transaction(self, transaction: TransactionCreate, token: str) -> TransactionResponse:
        try:
            response = requests.post(
                f"{self.api_base_url}/api/transactions/",
                json=transaction.dict(),
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return TransactionResponse(**response.json())
        except requests.exceptions.HTTPError as e:
            st.error(f"Transaction failed: {e.response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
        return None

    def get_transactions(self, token: str, skip: int = 0, limit: int = 100) -> List[TransactionResponse]:
        try:
            response = requests.get(
                f"{self.api_base_url}/api/transactions/?skip={skip}&limit={limit}",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return [TransactionResponse(**t) for t in response.json()]
        except Exception as e:
            st.error(f"Error loading transactions: {str(e)}")
            return []

    def get_transaction(self, transaction_id: int, token: str) -> TransactionResponse:
        try:
            response = requests.get(
                f"{self.api_base_url}/api/transactions/{transaction_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return TransactionResponse(**response.json())
        except Exception as e:
            st.error(f"Error loading transaction: {str(e)}")
            return None
        