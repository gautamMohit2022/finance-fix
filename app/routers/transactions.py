from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.transaction import (
    PaginatedTransactions, TransactionCreate,
    TransactionResponse, TransactionUpdate,
)
from app.services import transaction_service

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=201,
    summary="Add a transaction (Analyst / Admin)",
)
def create(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin, UserRole.analyst)),
):
    return transaction_service.create_transaction(db, data, current_user.id)


@router.get(
    "/",
    response_model=PaginatedTransactions,
    summary="List transactions with optional filters",
)
def list_transactions(
    transaction_type: Optional[str]  = Query(None, description="income or expense"),
    category:         Optional[str]  = Query(None, description="Filter by category"),
    start_date:       Optional[date] = Query(None, description="From date YYYY-MM-DD"),
    end_date:         Optional[date] = Query(None, description="To date YYYY-MM-DD"),
    skip:  int = Query(0,  ge=0),
    limit: int = Query(100, ge=1, le=200),   # FIX: raised default to 100 so frontend loads all
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return transaction_service.get_transactions(
        db=db,
        user_id=current_user.id,
        role=current_user.role.value,
        transaction_type=transaction_type,
        category=category,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{tid}",
    response_model=TransactionResponse,
    summary="Get a single transaction by ID",
)
def get_one(
    tid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return transaction_service.get_transaction_by_id(
        db, tid, current_user.id, current_user.role.value
    )


@router.put(
    "/{tid}",
    response_model=TransactionResponse,
    summary="Update a transaction (Analyst / Admin)",
)
def update(
    tid: int,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin, UserRole.analyst)),
):
    return transaction_service.update_transaction(
        db, tid, data, current_user.id, current_user.role.value
    )


@router.delete(
    "/{tid}",
    summary="Soft-delete a transaction (Admin only)",
)
def delete(
    tid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin)),
):
    return transaction_service.soft_delete_transaction(
        db, tid, current_user.id, current_user.role.value
    )
