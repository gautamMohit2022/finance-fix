from datetime import date
from calendar import monthrange
from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.transaction import Transaction, TransactionType


# ================= BASE QUERY (🔥 MOST IMPORTANT FIX) =================
def base_query(db: Session, user_id: int, role: str):
    query = db.query(Transaction).filter(Transaction.is_deleted == False)

    # 🔥 ROLE-BASED ACCESS
    if user_id is not None:
        query = query.filter(Transaction.user_id == user_id)

    return query


# ================= 1. OVERVIEW =================
def get_financial_overview(db: Session, user_id: int, role: str) -> dict:
    base = base_query(db, user_id, role)

    total_income = (
        base.filter(Transaction.type == TransactionType.income)
        .with_entities(func.sum(Transaction.amount))
        .scalar() or 0.0
    )

    total_expenses = (
        base.filter(Transaction.type == TransactionType.expense)
        .with_entities(func.sum(Transaction.amount))
        .scalar() or 0.0
    )

    balance = round(total_income - total_expenses, 2)
    savings_rate = round((balance / total_income * 100), 1) if total_income > 0 else 0.0

    income_count = base.filter(Transaction.type == TransactionType.income).count()
    expense_count = base.filter(Transaction.type == TransactionType.expense).count()

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "balance": balance,
        "savings_rate": savings_rate,
        "income_count": income_count,
        "expense_count": expense_count,
        "total_records": income_count + expense_count,
        "role": role,
    }


# ================= 2. CATEGORY BREAKDOWN =================
def get_category_breakdown(db: Session, user_id: int, role: str) -> dict:
    query = base_query(db, user_id, role).filter(
        Transaction.type == TransactionType.expense
    )

    rows = (
        query.with_entities(
            Transaction.category,
            func.sum(Transaction.amount).label("total"),
        )
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
        .all()
    )

    return {row.category: round(row.total, 2) for row in rows}


# ================= 3. MONTHLY TOTALS =================
def get_monthly_totals(db: Session, user_id: int, role: str) -> dict:
    query = base_query(db, user_id, role)

    rows = (
        query.with_entities(
            func.extract("year", Transaction.date).label("year"),
            func.extract("month", Transaction.date).label("month"),
            Transaction.type,
            func.sum(Transaction.amount).label("total"),
        )
        .group_by("year", "month", Transaction.type)
        .order_by("year", "month")
        .all()
    )

    monthly = defaultdict(lambda: {"income": 0.0, "expense": 0.0})

    for row in rows:
        key = f"{int(row.year)}-{int(row.month):02d}"
        monthly[key][row.type.value] = round(row.total, 2)

    result = {}
    for key, vals in monthly.items():
        result[key] = {
            "income": vals["income"],
            "expense": vals["expense"],
            "balance": round(vals["income"] - vals["expense"], 2),
        }

    return result


# ================= 4. RECENT ACTIVITY =================
def get_recent_activity(db: Session, user_id: int, role: str, limit: int = 5) -> list:
    query = base_query(db, user_id, role)

    txns = (
        query.order_by(Transaction.date.desc(), Transaction.created_at.desc())
        .limit(limit)
        .all()
    )

    result = []
    for t in txns:
        result.append({
            "id": t.id,
            "amount": t.amount,
            "type": t.type.value,
            "category": t.category,
            "date": str(t.date),
            "description": t.notes,
            "created_at": str(t.created_at),
        })

    return result


# ================= 5. TOP SPENDING =================
def get_top_spending_categories(db: Session, user_id: int, role: str, top_n: int = 5) -> list:
    query = base_query(db, user_id, role).filter(
        Transaction.type == TransactionType.expense
    )

    rows = (
        query.with_entities(
            Transaction.category,
            func.sum(Transaction.amount).label("total"),
        )
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
        .limit(top_n)
        .all()
    )

    grand_total = sum(r.total for r in rows) or 1

    return [
        {
            "category": r.category,
            "total": round(r.total, 2),
            "percentage": round((r.total / grand_total) * 100, 1),
        }
        for r in rows
    ]


# ================= 6. INCOME BREAKDOWN =================
def get_income_breakdown(db: Session, user_id: int, role: str) -> dict:
    query = base_query(db, user_id, role).filter(
        Transaction.type == TransactionType.income
    )

    rows = (
        query.with_entities(
            Transaction.category,
            func.sum(Transaction.amount).label("total"),
        )
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
        .all()
    )

    return {row.category: round(row.total, 2) for row in rows}


# ================= 7. CURRENT MONTH =================
def get_current_month_summary(db: Session, user_id: int, role: str) -> dict:
    today = date.today()
    month_start = today.replace(day=1)
    month_end = today.replace(day=monthrange(today.year, today.month)[1])

    base = base_query(db, user_id, role).filter(
        Transaction.date.between(month_start, month_end)
    )

    income = (
        base.filter(Transaction.type == TransactionType.income)
        .with_entities(func.sum(Transaction.amount))
        .scalar() or 0.0
    )

    expenses = (
        base.filter(Transaction.type == TransactionType.expense)
        .with_entities(func.sum(Transaction.amount))
        .scalar() or 0.0
    )

    cats = (
        base.filter(Transaction.type == TransactionType.expense)
        .with_entities(
            Transaction.category,
            func.sum(Transaction.amount).label("total"),
        )
        .group_by(Transaction.category)
        .all()
    )

    return {
        "month": today.strftime("%B %Y"),
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "balance": round(income - expenses, 2),
        "categories": {r.category: round(r.total, 2) for r in cats},
        "record_count": base.count(),
    }


# ================= 8. FULL SUMMARY =================
def get_full_summary(db: Session, user_id: int, role: str) -> dict:
    return {
        **get_financial_overview(db, user_id, role),
        "category_breakdown": get_category_breakdown(db, user_id, role),
        "income_breakdown": get_income_breakdown(db, user_id, role),
        "monthly_totals": get_monthly_totals(db, user_id, role),
        "recent_activity": get_recent_activity(db, user_id, role, 5),
        "top_spending": get_top_spending_categories(db, user_id, role, 5),
        "current_month": get_current_month_summary(db, user_id, role),
    }