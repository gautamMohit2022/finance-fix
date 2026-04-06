from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class BudgetCreate(BaseModel):
    category: str
    amount:   float       # stored as "amount" in DB now
    period:   str = "monthly"
    notes:    Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError("Budget amount must be greater than 0")
        return round(v, 2)

    @field_validator("category")
    @classmethod
    def category_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Category cannot be empty")
        return v.strip().title()


class BudgetResponse(BaseModel):
    id:         int
    category:   str
    amount:     float
    period:     str
    notes:      Optional[str] = None
    created_at: datetime
    user_id:    int

    model_config = {"from_attributes": True}
