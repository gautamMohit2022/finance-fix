import enum
from datetime import date, datetime
from sqlalchemy import Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class TransactionType(str, enum.Enum):
    income  = "income"
    expense = "expense"


class Transaction(Base):
    __tablename__ = "transactions"

    id         = Column(Integer, primary_key=True, index=True)
    amount     = Column(Float,   nullable=False)
    type       = Column(Enum(TransactionType), nullable=False)
    category   = Column(String(100), nullable=False, index=True)
    date       = Column(Date,    default=date.today, nullable=False, index=True)
    notes      = Column(Text,    nullable=True)       # stored as "notes" in DB
    is_deleted = Column(Boolean, default=False, nullable=False)  # soft delete flag
    created_at = Column(DateTime, default=datetime.utcnow,   nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,   nullable=False,
                        onupdate=datetime.utcnow)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="transactions")

    @property
    def description(self):
        """Alias so frontend 'description' field maps to DB 'notes'."""
        return self.notes

    @description.setter
    def description(self, value):
        self.notes = value

    def __repr__(self):
        return f"<Transaction id={self.id} type={self.type} amount={self.amount}>"
