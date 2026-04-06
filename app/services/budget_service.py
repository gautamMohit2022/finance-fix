from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.transaction import Transaction, TransactionType
from app.schemas.budget import BudgetCreate


def set_budget(db: Session, data: BudgetCreate, user_id: int) -> Budget:
    """Create or update budget for a category (upsert)."""
    existing = db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.category == data.category.title(),
    ).first()

    if existing:
        existing.amount = data.amount
        existing.period = data.period
        existing.notes  = data.notes
        db.commit()
        db.refresh(existing)
        return existing

    budget = Budget(
        category=data.category.title(),
        amount=data.amount,
        period=data.period,
        notes=data.notes,
        user_id=user_id,
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def get_budgets(db: Session, user_id: int):
    """Return all budgets for a user."""
    return db.query(Budget).filter(Budget.user_id == user_id).all()


def get_budget_by_id(db: Session, budget_id: int, user_id: int) -> Budget:
    budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == user_id,
    ).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


def update_budget(db: Session, budget_id: int, data: BudgetCreate, user_id: int) -> Budget:
    budget = get_budget_by_id(db, budget_id, user_id)
    if data.amount   is not None: budget.amount   = data.amount
    if data.category is not None: budget.category = data.category.title()
    if data.period   is not None: budget.period   = data.period
    if data.notes    is not None: budget.notes    = data.notes
    db.commit()
    db.refresh(budget)
    return budget


def delete_budget(db: Session, budget_id: int, user_id: int) -> dict:
    budget = get_budget_by_id(db, budget_id, user_id)
    db.delete(budget)
    db.commit()
    return {"message": f"Budget {budget_id} deleted"}


def get_budget_status(db: Session, user_id: int) -> list:
    """Compare each budget against actual spending this month."""
    today   = date.today()
    budgets = db.query(Budget).filter(Budget.user_id == user_id).all()
    results = []

    for b in budgets:
        spent = db.query(Transaction).filter(
            Transaction.user_id  == user_id,
            Transaction.type     == TransactionType.expense,
            Transaction.category == b.category,
            Transaction.is_deleted == False,
            Transaction.date.between(
                today.replace(day=1), today
            ),
        ).with_entities(
            __import__('sqlalchemy', fromlist=['func']).func.sum(Transaction.amount)
        ).scalar() or 0.0

        pct = round((spent / b.amount) * 100, 1) if b.amount else 0
        results.append({
            "id":        b.id,
            "category":  b.category,
            "limit":     b.amount,
            "amount":    b.amount,
            "spent":     round(spent, 2),
            "remaining": round(max(0, b.amount - spent), 2),
            "percent":   pct,
            "status":    "over" if pct >= 100 else "warning" if pct >= 80 else "ok",
            "period":    b.period,
            "notes":     b.notes,
        })

    return results
