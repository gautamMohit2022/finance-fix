import logging
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.services import summary_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/summary", tags=["Summary & Analytics"])


# ================= FULL SUMMARY =================
@router.get("")
def full_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info(f"Full summary requested by user_id={current_user.id} role={current_user.role}")

    # 🔥 ROLE-BASED ACCESS
    if current_user.role in [UserRole.admin, UserRole.analyst]:
        user_id = None
    else:
        user_id = current_user.id

    return summary_service.get_full_summary(db, user_id, current_user.role.value)


# ================= OVERVIEW =================
@router.get("/overview")
def overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info(f"Overview requested by user_id={current_user.id}")

    if current_user.role in [UserRole.admin, UserRole.analyst]:
        user_id = None
    else:
        user_id = current_user.id

    data = summary_service.get_financial_overview(db, user_id, current_user.role.value)
    return {"status": "success", "data": data}


# ================= RECENT =================
@router.get("/recent")
def recent(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info(f"Recent activity requested by user_id={current_user.id} limit={limit}")

    if current_user.role in [UserRole.admin, UserRole.analyst]:
        user_id = None
    else:
        user_id = current_user.id

    data = summary_service.get_recent_activity(db, user_id, current_user.role.value, limit)
    return {"status": "success", "data": data, "count": len(data)}


# ================= CATEGORY BREAKDOWN =================
@router.get("/categories")
def categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.analyst, UserRole.admin)),
):
    logger.info(f"Category breakdown requested by user_id={current_user.id}")

    # analyst + admin → ALL data
    data = summary_service.get_category_breakdown(db, None, current_user.role.value)

    return {"status": "success", "data": data}


# ================= INCOME BREAKDOWN =================
@router.get("/income-breakdown")
def income_breakdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.analyst, UserRole.admin)),
):
    logger.info(f"Income breakdown requested by user_id={current_user.id}")

    data = summary_service.get_income_breakdown(db, None, current_user.role.value)

    return {"status": "success", "data": data}


# ================= MONTHLY =================
@router.get("/monthly")
def monthly(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.analyst, UserRole.admin)),
):
    logger.info(f"Monthly totals requested by user_id={current_user.id}")

    data = summary_service.get_monthly_totals(db, None, current_user.role.value)

    return {"status": "success", "data": data}


# ================= CURRENT MONTH =================
@router.get("/current-month")
def current_month(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.analyst, UserRole.admin)),
):
    logger.info(f"Current month summary requested by user_id={current_user.id}")

    data = summary_service.get_current_month_summary(db, None, current_user.role.value)

    return {"status": "success", "data": data}


# ================= TOP SPENDING =================
@router.get("/top-spending")
def top_spending(
    top_n: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.analyst, UserRole.admin)),
):
    logger.info(f"Top spending requested by user_id={current_user.id} top_n={top_n}")

    data = summary_service.get_top_spending_categories(db, None, current_user.role.value, top_n)

    return {"status": "success", "data": data, "count": len(data)}