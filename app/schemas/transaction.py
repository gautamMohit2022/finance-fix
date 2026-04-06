from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, field_validator
from app.models.transaction import TransactionType


class TransactionCreate(BaseModel):
    amount: float
    type: TransactionType
    category: str
    date: date
    description: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return round(v, 2)

    @field_validator("category")
    @classmethod
    def category_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Category cannot be empty")
        return v.strip().title()


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    category: Optional[str] = None
    date: Optional[date] = None
    description: Optional[str] = None
    notes: Optional[str] = None


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: TransactionType
    category: str
    date: date
    description: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    user_id: int

    model_config = {"from_attributes": True}


class PaginatedTransactions(BaseModel):
    total: int
    skip: int
    limit: int
    transactions: List[TransactionResponse]