from datetime import date
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


# ================= CREATE =================
def create_transaction(db: Session, data: TransactionCreate, user_id: int) -> Transaction:
    notes = data.description or data.notes

    txn = Transaction(
        amount=data.amount,
        type=data.type,
        category=data.category,
        date=data.date,
        notes=notes,
        user_id=user_id,
    )

    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


# ================= LIST =================
def get_transactions(
    db: Session,
    user_id: Optional[int],   # 🔥 allow None
    role: str,
    transaction_type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 20,
) -> dict:

    # 🔥 FIX: base query
    query = db.query(Transaction).filter(Transaction.is_deleted == False)

    # 🔥 ROLE-BASED FILTER
    if role not in ["admin", "analyst"]:
        query = query.filter(Transaction.user_id == user_id)

    # ===== FILTERS =====
    if transaction_type:
        query = query.filter(Transaction.type == transaction_type)

    if category:
        query = query.filter(Transaction.category.ilike(f"%{category}%"))

    if start_date:
        query = query.filter(Transaction.date >= start_date)

    if end_date:
        query = query.filter(Transaction.date <= end_date)

    # ===== PAGINATION =====
    total = query.count()

    transactions = (
        query.order_by(Transaction.date.desc(), Transaction.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Add description field (maps from notes)
    for t in transactions:
        t.description = t.notes

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "transactions": transactions,
    }


# ================= GET ONE =================
def get_transaction_by_id(db: Session, tid: int, user_id: int, role: str) -> Transaction:
    txn = db.query(Transaction).filter(
        Transaction.id == tid,
        Transaction.is_deleted == False,
    ).first()

    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # 🔥 FIX: analyst can also see all
    if role not in ["admin", "analyst"] and txn.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    txn.description = txn.notes
    return txn


# ================= UPDATE =================
def update_transaction(
    db: Session, tid: int, data: TransactionUpdate, user_id: int, role: str
) -> Transaction:

    txn = get_transaction_by_id(db, tid, user_id, role)

    if data.amount is not None:
        txn.amount = data.amount

    if data.type is not None:
        txn.type = data.type

    if data.category is not None:
        txn.category = data.category.title()

    if data.date is not None:
        txn.date = data.date

    if data.description is not None:
        txn.notes = data.description
    elif data.notes is not None:
        txn.notes = data.notes

    db.commit()
    db.refresh(txn)
    txn.description = txn.notes

    return txn


# ================= DELETE =================
def soft_delete_transaction(db: Session, tid: int, user_id: int, role: str) -> dict:
    txn = get_transaction_by_id(db, tid, user_id, role)

    txn.is_deleted = True
    db.commit()

    return {"message": f"Transaction {tid} deleted successfully"}