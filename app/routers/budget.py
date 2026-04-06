from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetResponse
from app.services import budget_service

# FIX: was "/budgets" — changed to "/budget" to match frontend api.js calls
router = APIRouter(prefix="/budget", tags=["Budget Management"])


@router.post("/", response_model=BudgetResponse, status_code=201,
             summary="Create or update budget for a category")
def create_budget(
    data: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return budget_service.set_budget(db, data, current_user.id)


@router.get("/", response_model=List[BudgetResponse], summary="Get all budgets")
def list_budgets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return budget_service.get_budgets(db, current_user.id)


@router.get("/status", summary="Compare spending vs budget limits this month")
def budget_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return budget_service.get_budget_status(db, current_user.id)


@router.put("/{budget_id}", response_model=BudgetResponse, summary="Update a budget")
def update_budget(
    budget_id: int,
    data: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return budget_service.update_budget(db, budget_id, data, current_user.id)


@router.delete("/{budget_id}", summary="Delete a budget")
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return budget_service.delete_budget(db, budget_id, current_user.id)
