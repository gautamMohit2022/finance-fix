from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Budget(Base):
    """Monthly spending limit per category per user."""
    __tablename__ = "budgets"

    id         = Column(Integer, primary_key=True, index=True)
    category   = Column(String(100), nullable=False)
    amount     = Column(Float, nullable=False)          # FIX: was monthly_limit — renamed to amount for API consistency
    period     = Column(String(20), default="monthly")  # NEW: monthly / weekly / yearly
    notes      = Column(String(255), nullable=True)     # NEW: optional notes
    created_at = Column(DateTime, default=datetime.utcnow)

    # ForeignKey links each budget to a specific user.
    # This means User A's budgets are completely separate from User B's.
    # ON DELETE CASCADE — if user is deleted, their budgets are also deleted automatically.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="budgets")
